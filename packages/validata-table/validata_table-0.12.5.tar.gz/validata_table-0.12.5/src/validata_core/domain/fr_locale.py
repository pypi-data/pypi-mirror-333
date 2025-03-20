import re
from datetime import datetime
from typing import Any, List, Optional

from validata_core.domain.types import Locale, Translation

DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")


class FrLocale(Locale):
    def __repr__(self) -> str:
        return "FrLocale()"

    def required(self) -> Translation:
        return "Valeur manquante", "La valeur est obligatoire et doit être renseignée"

    def unique(self) -> Translation:
        return "Valeur dupliquée", "Les valeurs de cette colonne doivent être uniques"

    def min_length(self, cell_value: Any, min: Any) -> Translation:
        msg = (
            f"Le texte doit comporter au moins {min} caractère(s)"
            f" (au lieu de {len(cell_value)} actuellement)"
        )
        return "Valeur trop courte", msg

    def max_length(self, cell_value: Any, max: Any) -> Translation:
        msg = (
            f"Le texte ne doit pas comporter plus de {max}"
            f" caractère(s) (au lieu de {len(cell_value)} actuellement)"
        )
        return "Valeur trop longue", msg

    def minimum(self, cell_value: Any, min: Any) -> Translation:
        return "Valeur trop petite", f"La valeur doit être au moins égale à {min}"

    def maximum(self, cell_value: Any, max: Any) -> Translation:
        return "Valeur trop grande", f"La valeur doit être au plus égale à {max}"

    def pattern(
        self,
        cell_value: str,
        example: str,
        pattern: str,
    ) -> Translation:
        example_text = f"**Exemple valide** :\n{example}\n\n" if example else ""
        msg = (
            f"{cell_value} ne respecte pas le motif imposé\n\n"
            f"{example_text}"
            f"**Détails techniques** : la valeur doit respecter l'expression régulière `{pattern}`)"
        )
        return "Format incorrect", msg

    def enum(self, enum_values: Any) -> Translation:
        if len(enum_values) == 1:
            return "Valeur incorrecte", "L'unique valeur autorisée est {enum_values[0]}"

        else:
            md_str = "\n".join([f"- {val}" for val in enum_values])
            return (
                "Valeur incorrecte",
                f"Les valeurs autorisées sont :\n{md_str}",
            )

    def encoding(self) -> Translation:
        return (
            "Erreur d'encodage",
            "Un problème d'encodage empêche la lecture du fichier",
        )

    def missing_cell(self) -> Translation:
        return (
            "Cellule manquante",
            "La ligne n'a pas le même nombre de cellules que l'en-tête",
        )

    def unique_error(self) -> Translation:
        return "Valeur dupliquée", "Les valeurs de cette colonne doivent être uniques"

    def truncated_value(self) -> Translation:
        return "Valeur tronquée", "La cellule a possiblement été tronquée"

    def forbidden_value(self) -> Translation:
        return "Valeur interdite", "La cellule contient une valeur interdite"

    def sequential_value(self) -> Translation:
        return (
            "Valeur non séquentielle",
            "La cellule ne se conforme pas à la contrainte de valeurs séquentielles",
        )

    def ascii_value(self) -> Translation:
        return "Caractères non ASCII", "La cellule contient des caractères non ASCII"

    def extra_cell(self) -> Translation:
        return (
            "Valeur surnuméraire",
            "Le nombre de cellules de la ligne excède le nombre de colonnes défini dans le schéma",
        )

    def date_type(self, field_value: Any, expected_date_format: str) -> Translation:
        title = "Format de date incorrect"
        iso_format = "%Y-%m-%d"
        french_format = "%d/%m/%Y"
        display_format = (
            expected_date_format.replace("%Y", "aaaa")
            .replace("%y", "aa")
            .replace("%m", "mm")
            .replace("%d", "jj")
        )

        if expected_date_format == "default" or expected_date_format == "any":
            expected_date_format = iso_format

        if DATETIME_RE.match(field_value):
            field_value = field_value[: field_value.find("T")]

        input_format = None
        if _has_format(field_value, french_format):
            input_format = french_format

        if _has_format(field_value, iso_format):
            input_format = iso_format

        if input_format:
            formatted_value = _convert_date_to_format(
                field_value, input_format, expected_date_format
            )
            if formatted_value:
                message = (
                    f"La forme attendue est `{formatted_value}` (`{display_format}`)"
                )
                return title, message

        message = f"La date doit être écrite sous la forme `{display_format}`"

        return title, message

    def year_type(self, field_value: Any) -> Translation:
        msg = f"L'année doit être composée de 4 chiffres (valeur reçue : {field_value})"
        return "Format d'année incorrect", msg

    def number_type(self, field_value: Any) -> Translation:
        title = "Format de nombre incorrect"
        if "," in field_value:
            en_number = field_value.replace(",", ".")
            value_str = f"«&#160;{en_number}&#160;»"
            message = f"Le séparateur décimal à utiliser est le point ({value_str})"
        else:
            message = (
                "La valeur ne doit comporter que des chiffres"
                " et le point comme séparateur décimal"
            )
        return title, message

    def integer_type(self, field_value: Any) -> Translation:
        msg = f"La valeur doit être un nombre entier (valeur reçue : {field_value})"
        return "Format entier incorrect", msg

    def string_type(self, field_format: Any) -> Translation:
        title = "Format de texte incorrect"
        if field_format == "default":
            message = "La valeur doit être une chaîne de caractère"
        elif field_format == "uri":
            message = "La valeur doit être une adresse de page internet (URL)"
        elif field_format == "email":
            message = "La valeur doit être une adresse email"
        elif field_format == "binary":
            message = "La valeur doit être une chaîne encodée en base64"
        elif field_format == "uuid":
            message = "La valeur doit être un UUID"
        else:
            message = "La valeur doit être une chaîne de caractères"

        return title, message

    def boolean_type(
        self, true_values: List[str], false_values: List[str]
    ) -> Translation:
        true_values_str = et_join(list(map(lambda v: "`{}`".format(v), true_values)))
        false_values_str = et_join(list(map(lambda v: "`{}`".format(v), false_values)))
        title = "Valeur booléenne incorrecte"
        message = (
            f"Les valeurs acceptées sont {true_values_str} (vrai)"
            f" et {false_values_str} (faux)"
        )

        return title, message

    def array_type(self) -> Translation:
        return ("Tableau incorrecte", "La valeur doit être un tableau JSON valide")

    def missing_label(self, field_name: str) -> Translation:
        return (
            "Colonne manquante",
            f"La colonne obligatoire `{field_name}` est manquante",
        )

    def duplicate_labels(self) -> Translation:
        title = "En-têtes dupliquées"
        message = "Les en-têtes doivent être uniques"
        return title, message

    def blank_header(self) -> Translation:
        return "En-tête manquant", "La colonne n'a pas d'en-tête"

    def blank_row(self) -> Translation:
        return (
            "Ligne vide",
            "La ligne vide doit être retirée de la table",
        )

    def primary_key(self) -> Translation:
        return ("Clé primaire", "La cellule viole la contrainte de clé primaire")

    def foreign_key(self) -> Translation:
        return ("Clé étrangère", "La cellule viole la contrainte de clé étrangère")

    def duplicate_row(self) -> Translation:
        return ("Ligne dupliquée", "La ligne est dupliquée")

    def row_constraint(self) -> Translation:
        return (
            "Contrainte de ligne",
            "La ligne ne respecte pas la contrainte de ligne",
        )


def _has_format(date_string: str, date_format: str) -> bool:
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False


def _convert_date_to_format(
    date_string: str, input_date_format: str, output_date_format: str
) -> Optional[str]:
    try:
        return datetime.strptime(date_string, input_date_format).strftime(
            output_date_format
        )
    except ValueError:
        return None


def et_join(values: List[str]) -> str:
    """french enum
    >>> et_join([])
    ''
    >>> et_join(['a'])
    'a'
    >>> et_join(['a','b'])
    'a et b'
    >>> et_join(['a','b','c'])
    'a, b et c'
    >>> et_join(['a','b','c','d','e'])
    'a, b, c, d et e'
    """
    if not values:
        return ""
    if len(values) == 1:
        return values[0]
    return " et ".join([", ".join(values[:-1]), values[-1]])
