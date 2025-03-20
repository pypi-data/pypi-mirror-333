"""
Year Interval Value check

Vérifie que l'on a bien une valeur du type "aaaa/aaaa" avec la première année
inférieure à la seconde ou une année seulement
(si le paramètre allow-year-only est activé)

Messages d'erreur attendus :
- Si la valeur n'est pas du type ^\\d{4}/\\d{4}$ (ex : "toto")
  - La valeur "toto" n'a pas le format attendu pour une période (AAAA/AAAA).
- Si les deux années sont identiques (ex : "2017/2017")
  - Période "2017/2017 invalide. Les deux années doivent être différentes).
- Si la deuxième année est inférieure à la première (ex : "2017/2012")
  - Période "2017/2012" invalide. La deuxième année doit être postérieure
    à la première (2012/2017).

Pierre Dittgen, Jailbreak
"""

import re
from typing import Any

from validata_core.domain.check import Check
from validata_core.domain.types.error import Error
from validata_core.domain.types.error_types import ErrType
from validata_core.domain.validator import Validator, single_value

YEAR_INTERVAL_RE = re.compile(r"^(\d{4})/(\d{4})$")
YEAR_RE = re.compile(r"^\d{4}$")

# Module API


class YearInterval(Validator):
    """Year Interval Value check class."""

    def __init__(self, options):
        allow_year_only = options.declare("allow-year-only", str, "false")
        self._allow_year_only = allow_year_only in ("true", "yes")

    @single_value
    def validate(self, value: Any):
        rm = YEAR_INTERVAL_RE.match(value)

        if not rm:
            if not self._allow_year_only:
                return Error.new(
                    "Intervalle d'Années Incorrect",
                    "Format attendu : AAAA/AAAA",
                    ErrType.YEAR_INTERVAL_VALUE,
                )

            ym = YEAR_RE.match(value)

            if ym:
                return None

            return Error.new(
                "Intervalle d'Années Incorrect",
                "Format attendu : année (AAAA) ou intervale (AAAA/AAAA)",
                ErrType.YEAR_INTERVAL_VALUE,
            )

        year1 = int(rm.group(1))
        year2 = int(rm.group(2))

        if year1 == year2:
            return Error(
                "Intervalle d'Années Incorrect",
                "Les deux années doivent être différentes",
                ErrType.YEAR_INTERVAL_VALUE,
            )

        if year1 > year2:
            return Error(
                "Intervalle d'Années Incorrect",
                f"la deuxième année ({year1}) doit être postérieure à la première ({year2})",
                ErrType.YEAR_INTERVAL_VALUE,
            )


year_interval_value = Check("year-interval-value", YearInterval)
