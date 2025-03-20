"""
    Comme indiqué par Loïc Haÿ dans son mail du 5/7/2018

> Document de référence dans les spécifications SCDL :
> http://www.moselle.gouv.fr/content/download/1107/7994/file/nomenclature.pdf
>
> Dans la nomenclature Actes, les valeurs avant le "/" sont :
>
> Commande publique
> Urbanisme
> Domaine et patrimoine
> Fonction publique
> Institutions et vie politique
> Libertés publiques et pouvoirs de police
> Finances locales
> Domaines de compétences par thèmes
> Autres domaines de compétences
>
> Le custom check devra accepter minuscules et majuscules, accents et sans accents ...

    Pierre Dittgen, JailBreak
"""

import unicodedata

from validata_core.domain.check import Check
from validata_core.domain.types import Error, ErrType
from validata_core.domain.validator import BaseValidator, single_value


def norm_str(s):
    """Normalize string, i.e. removing accents and turning into lowercases"""
    return "".join(
        c
        for c in unicodedata.normalize("NFD", s.lower())
        if unicodedata.category(c) != "Mn"
    )


NORMALIZED_AUTHORIZED_VALUES = set(
    map(
        norm_str,
        [
            "Commande publique",
            "Urbanisme",
            "Domaine et patrimoine",
            "Fonction publique",
            "Institutions et vie politique",
            "Libertés publiques et pouvoirs de police",
            "Finances locales",
            "Domaines de compétences par thèmes",
            "Autres domaines de compétences",
        ],
    )
)


class NomenclatureActesValidator(BaseValidator):
    @single_value
    def validate(self, value):
        if "/" not in value:
            return Error.new(
                "Nomenclature Actes Invalide",
                "Le signe oblique « / » est manquant",
                ErrType.NOMENCLATURE_ACTES,
            )

        nomenc = value[: value.find("/")]

        # Nomenclature reconnue et pas d'espace avant ni après l'oblique
        if norm_str(nomenc) in NORMALIZED_AUTHORIZED_VALUES and "/ " not in value:
            return None
        if norm_str(nomenc.rstrip()) in NORMALIZED_AUTHORIZED_VALUES or "/ " in value:
            return Error.new(
                "Nomenclature Actes Invalide",
                "Le signe oblique ne doit pas être précédé ni suivi d'espace",
                ErrType.NOMENCLATURE_ACTES,
            )
        else:
            return Error.new(
                "Nomenclature Actes Invalide",
                f"Le préfixe de de l'acte {nomenc} n'est pas reconnu",
                ErrType.NOMENCLATURE_ACTES,
            )


nomenclature_actes = Check("nomenclature-actes-value", NomenclatureActesValidator)
