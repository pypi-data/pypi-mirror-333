"""
Compare columns value check

Pour deux colonnes données, si les deux comportent une valeur, vérifie que
la valeur de la première est :
- supérieure (>)
- supérieure ou égale (>=)
- égale (==)
- inférieure ou égale (<=)
- inférieure (<)
à la valeur de la deuxième colonne

Si les deux valeurs sont numériques, c'est une comparaison numérique
    qui est utilisée.
Si les deux valeurs ne sont pas numériques, c'est une comparaison lexicographique
    qui est utilisée.
Si une valeur est numérique et l'autre lexicographique, une erreur est relevée.

Paramètres :
- column : le nom de la première colonne
- column2 : le nom de la deuxième colonne
- op : l'opérateur de comparaison (">", ">=", "==", "<=" ou "<")

Messages d'erreur attendus :
- Opérateur [??] invalide
- La valeur de la colonne {col1} [{val1}] n'est pas comparable avec la valeur
    de la colonne {col2} [{val2}]
- La valeur de la colonne {col1} [{val1}] devrait être {opérateur} à la valeur
    de la colonne {col2} [{val2}]

Pierre Dittgen, Jailbreak
"""

import decimal
from typing import Any, Optional

from simpleeval import simple_eval

from validata_core.domain.check import Check
from validata_core.domain.types import Error, ErrType, Options
from validata_core.domain.validator import FieldValue, Validator

OP_LABELS = {
    ">": "supérieure",
    ">=": "supérieure ou égale",
    "==": "égale",
    "<=": "inférieure ou égale",
    "<": "inférieure",
}


class CompareColumns(Validator):
    def __init__(self, options: Options):
        self.op = options.declare("op", str)

        if self.op not in OP_LABELS:
            raise Exception(f"L'opérateur '{self.op}' n'est pas géré.")

    def validate(self, v1: FieldValue, v2: FieldValue):
        comparison_str = compute_comparison_str(v1.value, self.op, v2.value)

        if comparison_str is None:
            note = (
                f"La valeur de la colonne {v1.label} `{v1.value}`"
                " n'est pas comparable avec la valeur de la colonne"
                f" {v2.label} `{v2.value}`."
            )
            return Error.new(
                "Valeurs Non Comparables", note, ErrType.COMPARE_COLUMNS_VALUE
            )

        compare_result = simple_eval(comparison_str)
        if not compare_result:
            op_str = OP_LABELS[self.op]
            note = (
                f"La valeur de la colonne {v1.label} `{v1.value}` devrait"
                f" être {op_str} à la valeur de la colonne"
                f" {v2.label} `{v2.value}`."
            )
            return Error.new(
                "Erreur de Comparaison", note, ErrType.COMPARE_COLUMNS_VALUE
            )


compare_columns_check = Check(
    "compare-columns-value",
    validator_class=CompareColumns,
    field_params=["column", "column2"],
)


def compute_comparison_str(value1: Any, op: str, value2: Any) -> Optional[str]:
    """Computes comparison string

    If comparison is not possible, return None
    """

    # number vs number
    if is_a_number(value1) and is_a_number(value2):
        return f"{str(value1)} {op} {str(value2)}"

    # string vs string
    if isinstance(value1, str) and isinstance(value2, str):
        n_value1 = value1.replace('"', '\\"')
        n_value2 = value2.replace('"', '\\"')
        return f'"{n_value1}" {op} "{n_value2}"'

    # thing vs thing, compare string repr
    if type(value1) is type(value2):
        return f"'{value1}' {op} '{value2}'"

    # potato vs cabbage?
    return None


def is_a_number(value: Any) -> bool:
    """Return True if value is a number (int or float)
    or a string representation of a number.
    """
    if type(value) in (int, float) or isinstance(value, decimal.Decimal):
        return True
    if not isinstance(value, str):
        return False
    if value.isnumeric():
        return True
    try:
        float(value)
        return True
    except ValueError:
        return False
