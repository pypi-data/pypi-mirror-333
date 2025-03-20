"""Code related to table header management.

- schema_sync=True option disables all errors relative to
    (missing|extra|mismatch) header errors.
- Validata want to:
  - emit a missing header error if a required column is missing
  - emit warnings if:
    - a non required column is missing
    - an extra column has been added
    - columns are disordered
"""

from typing import Any, Generator

import frictionless

from validata_core.domain.types import Header


def iter_warnings(
    source_header: Header,
    required_field_names: list[str],
    schema: frictionless.Schema,
    ignore_header_case: bool,
) -> Generator[str, Any, Any]:
    """Iterate warnings in table."""
    schema_field_names = [field.name for field in schema.fields]

    def _to_lower(_list):
        return [s.lower() for s in _list]

    if ignore_header_case:
        schema_field_names = _to_lower(schema_field_names)
        source_header = _to_lower(source_header)
        required_field_names = _to_lower(required_field_names)

    # missing optional fields
    for field_name in schema_field_names:
        if field_name not in source_header and field_name not in required_field_names:
            yield f"Colonne manquante : Ajoutez la colonne manquante `{field_name}`."

    for h in source_header:
        if h not in schema_field_names:
            yield f"Colonne surnuméraire : Retirez la colonne `{h}` non définie dans le schéma."

    if (
        set(source_header) == set(schema_field_names)
        and source_header != schema_field_names
    ):
        yield f"Colonnes désordonnées : Réordonnez les colonnes du fichier pour respecter le schéma : {schema_field_names!r}."
