import opening_hours as opening_hours_lib

from validata_core.domain.check import Check
from validata_core.domain.types.error import Error
from validata_core.domain.types.error_types import ErrType
from validata_core.domain.validator import BaseValidator, single_value

error_msg = (
    "Horaires d'ouverture incorrects.\n\n"
    " La valeur doit respecter la spécification"
    " [OpenStreetMap](https://wiki.openstreetmap.org/wiki/Key:opening_hours)"
    " de description d'horaires d'ouverture."
)


class OpeningHours(BaseValidator):
    @single_value
    def validate(self, value):
        if not opening_hours_lib.validate(value):  # type: ignore
            return Error.new(
                "Horaires d'Ouverture Incorrects",
                error_msg,
                ErrType.OPENING_HOURS_VALUE,
            )


opening_hours = Check(
    "opening-hours-value",
    OpeningHours,
)
