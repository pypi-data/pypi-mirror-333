# -*- coding: utf-8 -*-
"""
Cohesive columns value check

Vérifie que pour une liste de colonnes donnée, toutes les colonnes ont une valeur
ou aucune des colonnes n'a une valeur.

Paramètres :
- column : la première colonne
- othercolumns : les autres colonnes qui doivent être remplies (ou non)

Messages d'erreur attendus :
- Les colonnes présentes parmi {liste des noms de colonnes} doivent toutes comporter une valeur
ou toutes être vides
"""

from typing import List, Sequence, Union

from validata_core.domain.check import Check, FieldParam
from validata_core.domain.types import Error, ErrType
from validata_core.domain.utils import flatten
from validata_core.domain.validator import BaseValidator, FieldValue


class CohesiveColumnsValue(BaseValidator):
    def validate(self, field: FieldValue, other_fields: List[FieldValue]):
        should_have_value = field.value is None

        if any((cell.value is None) != should_have_value for cell in other_fields):
            fields_labels = ", ".join([field.label] + [c.label for c in other_fields])
            note = (
                f"Les colonnes présentes parmi {fields_labels} doivent toutes comporter une valeur"
                " ou toutes être vides"
            )
            return Error.new(
                "Colonnes Non Solidaires", note, ErrType.COHESIVE_COLUMNS_VALUE
            )


def missing_fields_handler(
    expected_fields: Sequence[Union[str, List[str]]], observed_fields: List[str]
):
    flattenned_expected_fields: List[str] = flatten(expected_fields)
    missing_fields = set(flattenned_expected_fields) - set(observed_fields)
    if len(missing_fields) == 0 or set(flattenned_expected_fields) == set(
        missing_fields
    ):
        return None
    expected_str = ", ".join(f"'{field}'" for field in flattenned_expected_fields)
    missing_str = ", ".join(f"'{field}'" for field in missing_fields)
    return Error.new(
        "Colonnes Non Solidaires",
        f"Les colonnes { expected_str } doivent être soit toutes présentes, soit toutes absentes (sont absentes : { missing_str})",
        ErrType.COHESIVE_COLUMNS_VALUE,
    )


cohesive_columns_value = Check(
    "cohesive-columns-value",
    CohesiveColumnsValue,
    field_params=["column", FieldParam("othercolumns", holds_multiple=True)],
    skip_if_missing_values=False,
    missing_fields_handler=missing_fields_handler,
)
