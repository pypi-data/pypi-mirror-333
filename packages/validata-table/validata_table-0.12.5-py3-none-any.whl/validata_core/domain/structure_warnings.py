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

from typing import Dict


def structure_warning(
    code: str, name: str, message: str, field_name: str = ""
) -> Dict[str, str]:
    return {"code": code, "name": name, "message": message, "field_name": field_name}


def iter_structure_warnings(warning: str) -> Dict[str, str]:
    """Iterate structure warnings in formatted report."""

    # missing optional fields
    if "Colonne manquante : Ajoutez la colonne manquante " in warning:
        field_name = warning.split("`", 2)[1]
        return structure_warning(
            "missing-header-warn",
            "colonne manquante",
            f"Ajoutez la colonne manquante `{field_name}`.",
            field_name,
        )

    # extra header
    elif "Colonne surnuméraire : Retirez la colonne " in warning:
        field_name = warning.split("`", 2)[1]
        return structure_warning(
            "extra-header-warn",
            "colonne surnuméraire",
            f"Retirez la colonne `{field_name}` non définie dans le schéma.",
            field_name,
        )

    elif (
        "Colonnes désordonnées : Réordonnez les colonnes du fichier pour respecter le schéma : "
        in warning
    ):
        return structure_warning(
            "disordered-header-warn",
            "colonnes désordonnées",
            warning.split("Colonnes désordonnées : ", 2)[1],
        )

    else:
        return structure_warning(
            "unknown-warning", "warning inconnu", "Cause de warning inexpliquée."
        )
