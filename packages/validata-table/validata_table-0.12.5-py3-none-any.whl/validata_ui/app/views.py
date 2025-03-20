"""Routes."""

import inspect
import io
import json
import logging
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import (
    Any,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)
from urllib.parse import urlencode
from urllib.request import urlopen

import frictionless
import requests
from commonmark import commonmark
from flask import Request, abort, redirect, render_template, request, url_for
from flask_babel import _
from jsonschema import exceptions
from opendataschema import GitSchemaReference, SchemaCatalog, by_commit_date
from werkzeug.wrappers.response import Response

import validata_core.domain.types.table_region as table_region
from validata_core import resource_service as resource
from validata_core import validation_service
from validata_core.domain.table_resource import TableResource
from validata_core.domain.types import Error, Header, Report, Row, TypedException
from validata_ui.app import app, config, fetch_schema, schema_catalog_registry
from validata_ui.app.model import Section
from validata_ui.app.ui_util import ThreadUpdater, flash_error, flash_warning
from validata_ui.app.validata_util import strip_accents

log = logging.getLogger(__name__)

schema_catalog_updater: Dict[str, ThreadUpdater] = {}


class UIError(Error):
    def __init__(self, error: Error):
        super().__init__(
            _title=error._title,
            _message=error._message,
            type=error.type,
        )
        self.location = error.location
        self.tags = error.tags
        self.locale = error.locale
        self._validated_values = error._validated_values
        self._violated_constraint = error._violated_constraint
        self.content: str


@dataclass
class RowErrors:
    row_number: int
    errors: Dict[Union[str, int], UIError]  # str either field_labels or Literal["row"]


class UIReport(Report):
    def __init__(self, report: Report, headers: Header):
        super().__init__(
            report.errors,
            report.warnings,
            report.stats.seconds,
            report.stats.fields,
            report.stats.rows,
            report.stats.rows_processed,
        )
        self.headers = headers
        self.headers_title: List[str]
        self.headers_description: List[str]
        self.cols_alert: List[str]
        self.structure_errors: List[UIError] = []
        self.body_errors: List[UIError] = []
        self.body_errors_grouped_by_rows: List[RowErrors] = []
        self.count_by_code: Dict[str, int] = {}
        self.error_stats: Dict[str, int] = {}


def get_schema_catalog(section_name: str) -> SchemaCatalog:
    """Return a schema catalog associated to a section_name."""
    global schema_catalog_updater

    if section_name not in schema_catalog_updater:
        schema_catalog_updater[section_name] = ThreadUpdater(
            lambda: schema_catalog_registry.build_schema_catalog(section_name)
        )
    return schema_catalog_updater[section_name].value


class SchemaInstance:
    """Handy class to handle schema information."""

    def __init__(self, parameter_dict: Dict[str, Any]):
        """Initialize schema instance and tableschema catalog."""

        self.section_name = None
        self.section_title = None
        self.name = None
        self.url = None
        self.ref = None
        self.reference = None
        self.doc_url = None
        self.branches = None
        self.tags = None

        # From schema_url
        if parameter_dict.get("schema_url"):
            self.url = parameter_dict["schema_url"]
            self.section_title = _("Autre schéma")

        # from schema_name (and schema_ref)
        elif parameter_dict.get("schema_name"):
            self.schema_and_section_name = parameter_dict["schema_name"]
            self.ref = parameter_dict.get("schema_ref")

            # Check schema name
            chunks = self.schema_and_section_name.split(".")
            if len(chunks) != 2:
                abort(400, _("Paramètre 'schema_name' invalide"))

            self.section_name, self.name = chunks
            self.section_title = self.find_section_title(self.section_name)

            # Look for schema catalog first
            try:
                table_schema_catalog = get_schema_catalog(self.section_name)
            except Exception:
                log.exception("")
                abort(400, _("Erreur de traitement du catalogue"))
            if table_schema_catalog is None:
                abort(400, _("Catalogue indisponible"))

            schema_reference = table_schema_catalog.reference_by_name.get(self.name)
            if schema_reference is None:
                abort(
                    400,
                    f"Schéma {self.name!r} non trouvé dans le catalogue de la "
                    f"section {self.section_name!r}",
                )

            if isinstance(schema_reference, GitSchemaReference):
                self.tags = sorted(
                    schema_reference.iter_tags(), key=by_commit_date, reverse=True
                )
                if self.ref is None:
                    schema_ref = (
                        self.tags[0]
                        if self.tags
                        else schema_reference.get_default_branch()
                    )
                    abort(
                        redirect(
                            compute_validation_form_url(
                                {
                                    "schema_name": self.schema_and_section_name,
                                    "schema_ref": schema_ref.name,
                                }
                            )
                        )
                    )
                tag_names = [tag.name for tag in self.tags]
                self.branches = [
                    branch
                    for branch in schema_reference.iter_branches()
                    if branch.name not in tag_names
                ]
                self.doc_url = schema_reference.get_doc_url(
                    ref=self.ref
                ) or schema_reference.get_project_url(ref=self.ref)

            self.url = schema_reference.get_schema_url(ref=self.ref)

        else:
            flash_error(_("Erreur dans la récupération des informations de schéma"))
            abort(redirect(url_for("home")))

        try:
            self.schema = fetch_schema(self.url)
        except json.JSONDecodeError as e:
            err_msg = (
                _("Le schéma fourni n'est pas un fichier JSON valide") + f" : { e }"
            )
            log.exception(err_msg)
            flash_error(err_msg)
            abort(redirect(url_for("home")))
        except Exception as e:
            err_msg = _("Une erreur est survenue en récupérant le schéma") + f" : { e }"
            log.exception(err_msg)
            flash_error(err_msg)
            abort(redirect(url_for("home")))

    def request_parameters(self) -> Dict[str, Any]:
        """Build request parameter dict to identify schema."""
        return (
            {
                "schema_name": self.schema_and_section_name,
                "schema_ref": "" if self.ref is None else self.ref,
            }
            if self.name
            else {"schema_url": self.url}
        )

    def find_section_title(self, section_name: str) -> Optional[str]:
        """Return section title or None if not found."""
        if config.CONFIG:
            for section in config.CONFIG.homepage.sections:
                if section.name == section_name:
                    return section.title
        return None


def build_template_source_data(
    header: Header, rows: List[Row], preview_rows_nb: int = 5
) -> Dict[str, Any]:
    """Build source data information to preview in validation report page."""
    source_header_info = [(colname, False) for colname in header]

    rows_count = len(rows)
    preview_rows_count = min(preview_rows_nb, rows_count)
    return {
        "source_header_info": source_header_info,
        "header": header,
        "rows_nb": rows_count,
        "data_rows": rows,
        "preview_rows_count": preview_rows_count,
        "preview_rows": rows[:preview_rows_count],
    }


def build_ui_errors(errors: List[Error]) -> List[UIError]:
    """Add context to errors, converts markdown content to HTML."""

    def improve_err(err: Error) -> UIError:
        """Add context info based on row-nb presence and converts content to HTML."""
        ui_err = UIError(err)

        content = err.message
        ui_err.content = commonmark(content)

        return ui_err

    return [improve_err(err) for err in errors]


def get_headers_and_fields_dict_accounting_for_case_sensitivity(
    ignore_header_case: bool,
    headers: Sequence[str],
    fields_dict: Dict[Any, tuple[Any, Any]],
) -> Tuple[Sequence[str], Dict[Any, tuple[Any, Any]]]:
    """Returns a tuple including :
    - the list of headers, converted in lower case if case-insensitive,
    - the schema fields in dictionnary form, with name fields converted
    in lower case if case-insensitive.
    """

    if not ignore_header_case:
        return (
            headers,
            fields_dict,
        )
    else:
        return (
            [h.lower() for h in headers],
            {field.lower(): fields_dict[field] for field in fields_dict.keys()},
        )


def add_header_titles_and_description(
    ui_report: UIReport,
    fields_dict: Dict[Any, tuple[Any, Any]],
    headers: Sequence[str],
):
    """Add headers' titles and description to
    the UI report
    """

    ui_report.headers_title = [
        (fields_dict[h][0] if h in fields_dict else _("Colonne inconnue"))
        for h in headers
    ]

    ui_report.headers_description = [
        (
            fields_dict[h][1]
            if h in fields_dict
            else _("Cette colonne n'est pas définie dans le schema")
        )
        for h in headers
    ]


def add_columns_alerts(
    validata_report: Report,
    ui_report: UIReport,
    fields_dict: Dict[Any, tuple[Any, Any]],
    headers: Sequence[str],
):
    """Add columns alerts to the UI report"""

    missing_headers = []
    for err in validata_report.errors:
        if err.type == "missing-label":
            err_region = err.location
            assert table_region.involves_single_field(err_region)
            missing_headers.append(err_region.field_info.label)

    ui_report.cols_alert = [
        "table-danger" if h not in fields_dict or h in missing_headers else ""
        for h in headers
    ]


def group_errors_into_structure_and_body(
    ui_report: UIReport,
    errors: List[UIError],
):
    """Group errors into two disctinct groups 'structure' and 'body'
    in the UI report
    """
    for err in errors:
        if err.is_body_error():
            ui_report.body_errors.append(err)
        else:
            ui_report.structure_errors.append(err)


def group_body_errors_by_row_id(ui_report: UIReport):
    """Group body errorsby row id in the Ui report"""

    current_row_n = -1
    for err in ui_report.body_errors:
        if not table_region.involves_single_row(err.location):
            continue

        row_n = err.location.row_number

        is_new_row = row_n != current_row_n
        if is_new_row:
            current_row_n = row_n
            initial_error_counter = RowErrors(current_row_n, {})
            ui_report.body_errors_grouped_by_rows.append(initial_error_counter)

        if table_region.involves_single_field(err.location):
            field_pos = err.location.field_info.position
            ui_report.body_errors_grouped_by_rows[-1].errors[field_pos] = err
        else:
            ui_report.body_errors_grouped_by_rows[-1].errors["row"] = err


def sort_by_error_names_in_statistics(ui_report: UIReport):
    """Sort by error names in statistics UI report"""

    stats: Dict[str, Any] = {}

    def count_by_type(errs: List[UIError]):
        ct = Counter(err.title for err in errs)

        count = len(errs)
        count_by_type = sorted((k, v) for k, v in ct.items())
        return {"count": count, "count_by_type": count_by_type}

    stats = {
        "structure-errors": count_by_type(ui_report.structure_errors),
        "body-errors": count_by_type(ui_report.body_errors),
    }

    stats["body-errors"]["rows-count"] = len(ui_report.body_errors_grouped_by_rows)

    ui_report.error_stats = stats


def create_validata_ui_report(
    report: Report,
    schema_dict: Dict[str, Any],
    headers: Sequence[str],
    ignore_header_case: bool,
) -> UIReport:
    """Create an error report easier to handle and display using templates.

    improvements done:
    - only one table
    - errors are contextualized
    - error-counts is ok
    - errors are grouped by lines
    - errors are separated into "structure" and "body"
    - error messages are improved
    """
    ui_report = UIReport(report, headers)

    # Computes column info from schema
    fields_dict = {
        f["name"]: (f.get("title", f["name"]), f.get("description", ""))
        for f in schema_dict.get("fields", [])
    }

    (
        headers,
        fields_dict,
    ) = get_headers_and_fields_dict_accounting_for_case_sensitivity(
        ignore_header_case, headers, fields_dict
    )

    add_header_titles_and_description(
        ui_report,
        fields_dict,
        headers,
    )

    add_columns_alerts(
        report,
        ui_report,
        fields_dict,
        headers,
    )

    # prepare error structure for UI needs
    errors = build_ui_errors(report.errors)

    group_errors_into_structure_and_body(ui_report, errors)

    group_body_errors_by_row_id(ui_report)

    sort_by_error_names_in_statistics(ui_report)

    return ui_report


def iter_task_errors(
    report: Report, code_set: Optional[Set[str]] = None
) -> Generator[Error, Any, Any]:
    """Iterate on errors that prevent optimal validation."""
    yield from (
        err for err in report.errors if code_set is None or err.type in code_set
    )


def validate(
    schema_instance: SchemaInstance,
    table_resource: TableResource,
    ignore_header_case: bool,
) -> Union[Response, str]:
    """Validate source and display report."""

    def compute_resource_info(resource: TableResource):
        source = resource.source()
        return {
            "type": "url" if source.startswith("http") else "file",
            "url": source,
            "filename": Path(source).name,
        }

    # Call validata_core with parsed data
    validata_core_report = validation_service.validate_resource(
        table_resource, schema_instance.schema, ignore_header_case
    )

    # Handle pre-validation errors
    pre_validation_errors, redirected_url = handle_unviewable_errors(
        table_resource, validata_core_report, schema_instance
    )

    if pre_validation_errors:
        return redirect(redirected_url)

    # # handle report date
    report_datetime = datetime.fromisoformat(
        validata_core_report.metadata.date
    ).astimezone()

    headers = table_resource.header()
    # create ui_report
    ui_report = create_validata_ui_report(
        validata_core_report,
        schema_instance.schema,
        headers,
        ignore_header_case,
    )

    # Display report to the user
    validator_form_url = compute_validation_form_url(
        schema_instance.request_parameters()
    )
    schema_info = extract_schema_metadata(schema_instance.schema)

    return render_template(
        "validation_report.html",
        config=config,
        badge_msg=None,
        badge_url=None,
        breadcrumbs=[
            {"title": _("Accueil"), "url": url_for("home")},
            {"title": schema_instance.section_title},
            {
                "title": schema_info.title,
                "url": validator_form_url,
            },
            {"title": _("Rapport de validation")},
        ],
        display_badge=False,
        doc_url=schema_instance.doc_url,
        print_mode=request.args.get("print", "false") == "true",
        report=ui_report,
        schema_current_version=schema_instance.ref,
        schema_info=schema_info,
        section_title=schema_instance.section_title,
        source_data=build_template_source_data(
            table_resource.header(), table_resource.rows()
        ),
        resource=compute_resource_info(table_resource),
        validation_date=report_datetime.strftime("le %d/%m/%Y à %Hh%M"),
    )


def handle_unviewable_errors(
    table_resource: TableResource,
    validata_core_report: Report,
    schema_instance: SchemaInstance,
) -> Tuple[List[Error], str]:
    """This function aims to renders an explicte flash message error when some specific
    errors occure in the validation report which are unviewable in the data tabular visualization.
    Specific errors handled in this function are:
    - `Error` with this specific message '"schema_sync" requires unique labels in the header'
    - `SchemaError`
    - `CheckError
    - `SourceError`

    """

    pre_validation_errors = list(
        iter_task_errors(
            validata_core_report,
            {
                "error",
                "schema-error",
                "check-error",
                "source-error",
            },
        )
    )

    redirected_url = compute_validation_form_url(schema_instance.request_parameters())

    flash_message_error_set = set()

    for error in pre_validation_errors:
        # Error with duplicated labels in header
        if error.type == "error" and (
            '"schema_sync" requires unique labels in the header' in error.message
        ):
            flash_message_error_set.add(
                f"Le fichier '{Path(table_resource.source()).name}' comporte des colonnes avec le même nom. "
                "Pour valider le fichier, veuillez d'abord le corriger en mettant des valeurs uniques dans "
                "son en-tête (la première ligne du fichier)."
            )

        # 'SchemaError' occurs in frictionless report in these cases :
        # - a field name does not exist in the schema
        # - a field name is not unique in the schema
        # - a primary key does not match the corresponding schema fields
        # - a foreign key does not match the corresponding schema fields
        # - foreign key fields does not match the reference fields
        if error.type == "schema-error":
            flash_message_error_set.add(
                "Erreur de schéma : Le schéma n'est pas valide selon la spécification TableSchema."
            )

        if error.type == "check-error":
            flash_message_error_set.add(
                'Erreur de "custom_checks" : ' f"{error.message}"
            )

        if error.type == "source-error":
            msg = (
                _("l'encodage du fichier est invalide. Veuillez le corriger.")
                if "charmap" in error.message
                else error.message
            )
            flash_message_error_set.add("Erreur de source : {}.".format(msg))
            redirected_url = url_for("custom_validator")

    flash_message_error = " - ".join(flash_message_error_set)

    if flash_message_error_set:
        flash_error(f"Validation annulée : {flash_message_error}")

    return pre_validation_errors, redirected_url


def bytes_data(f) -> bytes:
    """Get bytes data from Werkzeug FileStorage instance."""
    iob = io.BytesIO()
    f.save(iob)
    iob.seek(0)
    return iob.getvalue()


def retrieve_schema_catalog(
    section: Section,
) -> Tuple[Optional[SchemaCatalog], Optional[Dict[str, Any]]]:
    """Retrieve schema catalog and return formatted error if it fails."""

    def format_error_message(err_message: str, exc: Exception) -> str:
        """Prepare a bootstrap error message with details if wanted."""
        exception_text = "\n".join([str(arg) for arg in exc.args])

        return f"""{err_message}
        <div class="float-right">
            <button type="button" class="btn btn-info btn-xs" data-toggle="collapse"
                data-target="#exception_info">détails</button>
        </div>
        <div id="exception_info" class="collapse">
                <pre>{exception_text}</pre>
        </div>
"""

    try:
        schema_catalog = get_schema_catalog(section.name)
        return (schema_catalog, None)

    except Exception as exc:
        err_msg = "une erreur s'est produite"
        if isinstance(exc, requests.ConnectionError):
            err_msg = _("problème de connexion")
        elif isinstance(exc, json.decoder.JSONDecodeError):
            err_msg = _("format JSON incorrect")
        elif isinstance(exc, exceptions.ValidationError):
            err_msg = _("le catalogue ne respecte pas le schéma de référence")
        log.exception(err_msg)

        error_catalog = {
            **{k: v for k, v in section.dict().items() if k != "catalog"},
            "err": format_error_message(err_msg, exc),
        }
        return None, error_catalog


# Routes


def iter_sections() -> Iterable[Union[Section, Optional[Dict[str, Any]]]]:
    """Yield sections of the home page, filled with schema metadata."""
    # Iterate on all sections
    for section in config.CONFIG.homepage.sections:
        # section with only links to external validators
        if section.links:
            yield section
            continue

        # section with catalog
        if section.catalog is None:
            # skip section
            continue

        # retrieving schema catatalog
        schema_catalog, catalog_error = retrieve_schema_catalog(section)
        if schema_catalog is None:
            yield catalog_error
            continue

        # Working on catalog
        schema_info_list = []
        for schema_reference in schema_catalog.references:
            # retain tableschema only
            if schema_reference.get_schema_type() != "tableschema":
                continue

            # Loads default table schema for each schema reference
            schema_info: Dict[str, Any] = {"name": schema_reference.name}
            try:
                table_schema = fetch_schema(schema_reference.get_schema_url())
            except json.JSONDecodeError:
                schema_info["err"] = True
                schema_info["title"] = (
                    f"le format du schéma « {schema_info['name']} » "
                    "n'est pas reconnu"
                )
            except Exception:
                schema_info["err"] = True
                schema_info["title"] = (
                    f"le schéma « {schema_info['name']} » " "n'est pas disponible"
                )
            else:
                schema_info["title"] = table_schema.get("title") or schema_info["name"]
            schema_info_list.append(schema_info)
        schema_info_list = sorted(
            schema_info_list, key=lambda sc: strip_accents(sc["title"].lower())
        )

        yield {
            **{k: v for k, v in section.dict().items() if k != "catalog"},
            "catalog": schema_info_list,
        }


section_updater = ThreadUpdater(lambda: list(iter_sections()))


@app.route("/")
def home():
    """Home page."""

    return render_template("home.html", config=config, sections=section_updater.value)


@dataclass
class SchemaMetadata:
    title: str
    version: Optional[str] = None
    resources: Optional[Dict[str, str]] = None
    contributors: Optional[Dict[str, str]] = None
    description: Optional[str] = None
    homepage: Optional[str] = None

    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]) -> "SchemaMetadata":
        dict_.setdefault("title", _("Schéma sans titre"))

        return cls(
            **{
                k: v for k, v in dict_.items() if k in inspect.signature(cls).parameters
            },
        )


def extract_schema_metadata(table_schema: dict) -> SchemaMetadata:
    """Parses the metadata from the schema descriptor.

    A default value is set to `title` if missing.
    """
    metadata_dict = {k: v for k, v in table_schema.items() if k != "fields"}

    return SchemaMetadata.from_dict(metadata_dict)


def compute_validation_form_url(request_parameters: Dict[str, Any]) -> str:
    """Compute validation form url with schema URL parameter."""
    url = url_for("custom_validator")
    return "{}?{}".format(url, urlencode(request_parameters))


def redirect_url_if_needed(url_param: str) -> str:
    """
    Redirects the url of url_param to its static url and
    returns this url.
    If url_param is already a static url, there is no
    url redirection, and it returns its value.

    :param url_param: str : url to redirect
    :return: str: redirected url
    """

    redirected_url = urlopen(url_param).geturl()
    return redirected_url


def get_ignore_header_case_from_checkbox(req: Request) -> bool:
    """
    Get the value of the "ignore-header-case" checkbox.
    The value is stored as a query string parameter or in the
    request body, depending on the method used for the form
    submit (GET or POST respectively).
    """
    ignore_header_case = req.form.get(
        "ignore-header-case", type=bool, default=False
    ) or req.args.get("ignore-header-case", type=bool, default=False)
    return ignore_header_case


@app.route("/table-schema", methods=["GET", "POST"])
def custom_validator() -> Union[str, Response, Tuple[str, int]]:
    """Display validator form."""
    if request.method == "GET":
        # input is a hidden form parameter to know
        # if this is the initial page display or if the validation has been asked for
        input_param = request.args.get("input")

        # url of resource to be validated
        url_param = request.args.get("url")

        schema_instance = SchemaInstance(request.args)

        try:
            schema_validation_report = validation_service.validate_schema(
                schema_instance.schema
            )
        except frictionless.exception.FrictionlessException as e:
            flash_error(f"Une erreur est survenue pendant la validation du schéma: {e}")
            return redirect(url_for("home"))

        errors = schema_validation_report.errors
        if errors:
            if "schema_url" in request.args:
                flash_error(
                    "Le schéma fourni est invalide.\n"
                    f"Erreurs survenues lors de la validation : {  [e.message for e in errors] }"
                )

            elif "schema_name" in request.args:
                flash_error(
                    f"Le schéma choisi '{schema_instance.schema['title']}', "
                    f"version '{schema_instance.schema['version']}' est invalide."
                    "Veuillez choisir une autre version ou contacter le mainteneur du schéma."
                )

            return redirect(url_for("home"))

        # First form display
        if input_param is None:
            schema_info = extract_schema_metadata(schema_instance.schema)
            return render_template(
                "validation_form.html",
                config=config,
                branches=schema_instance.branches,
                breadcrumbs=[
                    {"url": url_for("home"), "title": "Accueil"},
                    {"title": schema_instance.section_title},
                    {"title": schema_info.title},
                ],
                doc_url=schema_instance.doc_url,
                schema_current_version=schema_instance.ref,
                schema_info=schema_info,
                schema_params=schema_instance.request_parameters(),
                section_title=schema_instance.section_title,
                tags=schema_instance.tags,
            )

        # Process URL
        else:
            validation_form_url = compute_validation_form_url(
                schema_instance.request_parameters()
            )

            if not url_param:
                flash_error(_("Vous n'avez pas indiqué d'URL à valider"))
                return redirect(validation_form_url)
            try:
                url = redirect_url_if_needed(url_param)
                table_resource = resource.from_remote_file(url)
            except Exception as ex:
                flash_error(
                    f"Une erreur s'est produite en récupérant les données : {ex}"
                )
                return redirect(validation_form_url)

            try:
                ignore_header_case = get_ignore_header_case_from_checkbox(request)
                return validate(
                    schema_instance,
                    table_resource,
                    ignore_header_case=ignore_header_case,
                )
            except Exception as ex:
                flash_error(f"Une erreur s'est produite en validant les données : {ex}")
                return redirect(validation_form_url)

    elif request.method == "POST":
        schema_instance = SchemaInstance(request.form)

        input_param = request.form.get("input")
        if input_param is None:
            flash_error(_("Vous n'avez pas indiqué de fichier à valider"))
            return redirect(
                compute_validation_form_url(schema_instance.request_parameters())
            )

        # File validation
        if input_param == "file":
            f = request.files.get("file")
            if f is None:
                flash_warning(_("Vous n'avez pas indiqué de fichier à valider"))
                return redirect(
                    compute_validation_form_url(schema_instance.request_parameters())
                )
            try:
                table_resource = resource.from_file_content(
                    f.filename or "", bytes_data(f)
                )
            except TypedException as err:
                flash_error(
                    "Une erreur s'est produite à la lecture du fichier."
                    " Veuillez vérifier que le fichier est valide."
                    f" Erreur de type { err.type.value } : { str(err) }"
                )
                return redirect(
                    compute_validation_form_url(schema_instance.request_parameters())
                )
            ignore_header_case = get_ignore_header_case_from_checkbox(request)
            return validate(
                schema_instance,
                table_resource,
                ignore_header_case=ignore_header_case,
            )

        return _("Combinaison de paramètres non supportée"), 400

    else:
        return "Method not allowed", 405
