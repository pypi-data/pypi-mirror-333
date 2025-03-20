# -*- coding: utf-8 -*-
"""
One of required check

Ce custom check vérifie :
- Pour les deux colonnes relatives à ce custom check, pour une ligne donnée, au moins une des deux colonnes doit
contenir une valeur,
- Pour une ligne donnée, les deux colonnes peuvent contenir chacune une valeur,
- Si une des deux colonnes est manquantes, alors toute valeur manquante dans l'autre colonne engendre une erreur de
validation,
- Si les deux colonnes sont manquantes cela engendre une erreur de validation.


Paramètres :
- column1 : la première colonne
- column2 : la deuxième colonne

Messages d'erreur attendus :
- Les colonnes {nom de la première colonne} et {nom de la deuxième colonne} sont manquantes.
- Au moins l'une des colonnes {liste des noms de colonnes} doit comporter une valeur.

Amélie Rondot, multi
"""

from typing import List, Sequence, Union

from validata_core.domain.check import Check
from validata_core.domain.types import Error, ErrType
from validata_core.domain.utils import flatten
from validata_core.domain.validator import BaseValidator, FieldValue


class OneOfRequired(BaseValidator):
    def validate(self, field1: FieldValue, field2: FieldValue):
        if not field1.value and not field2.value:
            return Error.new(
                "Un Élement Requis",
                f"Au moins l'une des colonnes '{field1.label}' ou '{field2.label}' doit comporter une valeur",
                ErrType.ONE_OF_REQUIRED,
            )


def missing_fields_handler(
    expected_fields: Sequence[Union[str, List[str]]], observed_fields: List[str]
):
    flattenned_expected_fields: List[str] = flatten(expected_fields)
    missing_fields = set(flattenned_expected_fields) - set(observed_fields)
    if len(missing_fields) == 2:
        missing_str = " et ".join(f"'{field}'" for field in sorted(missing_fields))
        return Error.new(
            "Un Élement Requis",
            f"Une des deux colonnes requise : {missing_str} sont manquantes",
            ErrType.ONE_OF_REQUIRED,
        )


one_of_required = Check(
    "one-of-required",
    OneOfRequired,
    ["column1", "column2"],
    skip_if_missing_values=False,
    missing_fields_handler=missing_fields_handler,
)
