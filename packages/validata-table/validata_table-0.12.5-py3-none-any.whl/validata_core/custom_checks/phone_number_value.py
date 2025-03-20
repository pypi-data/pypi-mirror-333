import phonenumbers

from validata_core.domain.check import Check
from validata_core.domain.types.error import Error
from validata_core.domain.types.error_types import ErrType
from validata_core.domain.validator import BaseValidator, single_value

error_msg = (
    "Numéro de téléphone invalide.\n\n"
    " Les numéros de téléphone acceptés sont les numéros français à 10 chiffres"
    " (`01 99 00 27 37`) ou au format international avec le préfixe du pays"
    " (`+33 1 99 00 27 37`). Les numéros courts (`115` ou `3949`) sont"
    " également acceptés."
)


class PhoneNumber(BaseValidator):
    @single_value
    def validate(self, value):
        """Check if a phone number is a french or international valid one."""
        if not self._is_valid_number_for_country(
            value, country_code="FR"
        ) and not self._is_valid_number_for_country(value):
            return Error.new(
                "Numéro de Téléphone Incorrect", error_msg, ErrType.PHONE_NUMBER_VALUE
            )

    def _is_valid_number_for_country(self, phone_number: str, *, country_code=None):
        """Check if a phone number, giving an optional country_code.

        If country code is given, an additional check for valid_short_number is done.
        """
        try:
            pn = phonenumbers.parse(phone_number, country_code)
        except phonenumbers.NumberParseException:
            return False

        std_valid = phonenumbers.is_valid_number(pn)
        return (
            std_valid
            if country_code is None
            else std_valid or phonenumbers.is_valid_short_number(pn)
        )


phone_number = Check(
    "phone-number-value",
    PhoneNumber,
)
