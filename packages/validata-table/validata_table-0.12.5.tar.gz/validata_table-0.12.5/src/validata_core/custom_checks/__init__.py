from validata_core.domain.check import new_check_repository

from .cohesive_columns_value import cohesive_columns_value
from .compare_columns_value import compare_columns_check
from .french_gps_coordinates import french_gps_coordinates
from .nomenclature_actes_value import nomenclature_actes
from .one_of_required import one_of_required
from .opening_hours_value import opening_hours
from .phone_number_value import phone_number
from .sum_columns_value import columns_sum
from .year_interval_value import year_interval_value

# from .year_interval_value import YearIntervalValue

# Please keep the below dict up-to-date

_available_checks = [
    cohesive_columns_value,
    compare_columns_check,
    french_gps_coordinates,
    nomenclature_actes,
    opening_hours,
    phone_number,
    columns_sum,
    year_interval_value,
    one_of_required,
]


validata_check_repository = new_check_repository(_available_checks)
