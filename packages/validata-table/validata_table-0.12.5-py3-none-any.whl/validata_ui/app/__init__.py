"""Validata UI."""

import logging
from datetime import timedelta

import flask
import importlib_metadata
import jinja2
import opendataschema
import requests
import requests_cache
from commonmark import commonmark
from flask_babel import Babel
from pydantic import BaseModel, HttpUrl
from pydantic_core import Url

from validata_core.domain.types import SchemaDescriptor
from validata_ui.app import config
from validata_ui.app.locale import get_locale

log = logging.getLogger(__name__)


def generate_schema_from_url_func(session):
    """Generates a function that encloses session"""

    def fetch_schema(url: str) -> SchemaDescriptor:
        response = session.get(url)
        response.raise_for_status()
        schema_descriptor = response.json()
        return schema_descriptor

    return fetch_schema


class SchemaCatalogRegistry:
    """Retain section_name -> catalog url matching
    and creates SchemaCatalog instance on demand"""

    def __init__(self, session):
        self.session = session
        self.ref_map = {}

    def add_ref(self, name, ref):
        self.ref_map[name] = ref

    def build_schema_catalog(self, name):
        ref = self.ref_map.get(name)
        if not ref:
            return None
        return opendataschema.SchemaCatalog(ref, session=self.session)


caching_session = requests.Session()
if config.CACHE_EXPIRE_AFTER != 0:
    expire_after = timedelta(minutes=float(config.CACHE_EXPIRE_AFTER))
    caching_session = requests_cache.CachedSession(
        backend=config.CACHE_BACKEND,
        cache_name="validata_ui_cache",
        expire_after=expire_after,
    )

fetch_schema = generate_schema_from_url_func(caching_session)

# And load schema catalogs which URLs are found in 'homepage' key of config.yaml
schema_catalog_registry = SchemaCatalogRegistry(caching_session)
if config.CONFIG:
    log.info("Initializing homepage sections...")
    for section in config.CONFIG.homepage.sections:
        name = section.name
        log.info('Initializing homepage section "{}"...'.format(name))

        if section.catalog:
            # Test if section.catalog is an instance of pydantic.HttpUrl
            # (https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.HttpUrl)
            catalog_ref = (
                str(section.catalog)
                if (
                    isinstance(section.catalog, Url)
                    or isinstance(section.catalog, HttpUrl)
                )
                else (
                    section.catalog.model_dump()
                    if isinstance(section.catalog, BaseModel)  # Dump model
                    else section.catalog
                )
            )
            schema_catalog_registry.add_ref(name, catalog_ref)
    log.info("...done")


def configure_sentry(app):
    """Configure sentry.io service for application error monitoring."""

    sentry_dsn = app.config.get("SENTRY_DSN")
    if sentry_dsn:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration

        sentry_sdk.init(dsn=sentry_dsn, integrations=[FlaskIntegration()])


# Flask things
app = flask.Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY
configure_sentry(app)

babel = Babel(app, locale_selector=get_locale)

# Jinja2 url_quote_plus custom filter
# https://stackoverflow.com/questions/12288454/how-to-import-custom-jinja2-filters-from-another-file-and-using-flask
blueprint = flask.Blueprint("filters", __name__)


@jinja2.pass_context
@blueprint.app_template_filter()
def commonmark2html(context, value):
    if not value:
        return value
    try:
        return commonmark(value)
    except Exception as ex:
        log.exception(ex)
        return value


app.register_blueprint(blueprint)


@app.context_processor
def inject_version():
    try:
        version = importlib_metadata.version("validata-table")
    except importlib_metadata.PackageNotFoundError:
        version = (
            "Numéro de version uniquement disponible si le package "
            "validata-table est installé"
        )
    return {"validata_ui_version": version}


@app.context_processor
def inject_config():
    return {"config": config}


# Keep this import after app initialisation (to avoid cyclic imports)
from validata_ui.app import views  # noqa: E402, F401
