"""
Sum columns value check

Pour une colonne donnée (column) et une liste de colonnes (columns),
on vérifie que la première colonne contient bien
la somme des valeurs entières des autres colonnes

La vérification ne s'effectue pas si l'ensemble des colonnes est vide

Paramètres :
- column : le nom de la première colonne contenant la somme
- columns : le nom des colonnes contenant les valeurs à ajouter

Messages d'erreur attendus :
- La valeur de la colonne {col} [val] n'est pas entière, il n'est pas possible
    de vérifier que {col} = {col1} + {col2} + ...
- La valeur des colonnes {col1}, {col2}, ... ne sont pas entières,
    il n'est pas possible de vérifier que {col} = {col1} + {col2} + ...
- La somme des valeurs des colonnes {col1}, {col2}, ... est {sum},
    ce nombre est différent de celui attendu dans {col} [val]

Pierre Dittgen, Jailbreak
"""

from typing import List

from validata_core.domain.check import Check, FieldParam
from validata_core.domain.types.error import Error
from validata_core.domain.types.error_types import ErrType
from validata_core.domain.validator import BaseValidator, FieldValue


class ColumnsSum(BaseValidator):
    """Sum columns value check."""

    def validate(self, expected_sum_field: FieldValue, fields: List[FieldValue]):
        computed_sum = sum(f.value for f in fields)

        if computed_sum != expected_sum_field.value:
            fields_str = ", ".join(f.label for f in fields)
            error_msg = (
                f"La somme des valeurs des colonnes {fields_str}"
                f" ({computed_sum}) est différent de celui trouvé"
                f" dans la colonne {expected_sum_field.label} ({expected_sum_field.value})"
            )
            return Error.new(
                "Somme de Colonnes Incorrecte", error_msg, ErrType.SUM_COLUMNS_VALUE
            )


columns_sum = Check(
    "sum-columns-value",
    ColumnsSum,
    [
        "column",
        FieldParam("columns", holds_multiple=True),
    ],
)
