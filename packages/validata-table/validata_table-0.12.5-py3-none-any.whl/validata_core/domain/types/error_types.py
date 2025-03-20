from enum import Enum


class ErrType(Enum):
    """Type of error

    For a new class error, create a new type rather than using an existing
    one.

    Indeed, each type comes with a number of expectations, which you can read more
    about in the error.py file. Do not an existing type without meeting these requirements,
    as this may lead to errors.
    """

    ERROR = "error"

    # frictionless/errors/cell.py
    CELL_ERROR = "cell-error"
    EXTRA_CELL = "extra-cell"
    MISSING_CELL = "missing-cell"
    TYPE_ERROR = "type-error"
    CONSTRAINT_ERROR = "constraint-error"
    UNIQUE_ERROR = "unique-error"
    TRUNCATED_VALUE = "truncated-value"
    FORBIDDEN_VALUE = "forbidden-value"
    SEQUENTIAL_VALUE = "sequential-value"
    ASCII_VALUE = "ascii-value"

    # frictionless/errors/data.py
    DATA_ERROR = "data-error"

    # frictionless/errors/file.py
    FILE_ERROR = "file-error"
    HASH_COUNT = "hash-count"
    BYTE_COUNT = "byte-count"

    # frictionless/errors/header.py
    HEADER_ERROR = "header-error"
    BLANK_HEADER = "blank-header"

    # frictionless/errors/label.py
    LABEL_ERROR = "label-error"
    EXTRA_LABEL = "extra-label"
    MISSING_LABEL = "missing-label"
    BLANK_LABEL = "blank-label"
    DUPLICATE_LABEL = "duplicate-label"
    INCORRECT_LABEL = "incorrect-label"

    # frictionless/errors/metadata.py
    METADATA_ERROR = "metadata-error"
    CATALOG_ERROR = "catalog-error"
    DATASET_ERROR = "dataset-error"
    CHECKLIST_ERROR = "checklist-error"
    CHECK_ERROR = "check-error"
    DETECTOR_ERROR = "detector-error"
    DIALECT_ERROR = "dialect-error"
    CONTROL_ERROR = "control-error"
    INQUIRY_ERROR = "inquiry-error"
    INQUIRY_TASK_ERROR = "inquiry-task-error"
    PACKAGE_ERROR = "package-error"
    PIPELINE_ERROR = "pipeline-error"
    STEP_ERROR = "step-error"
    REPORT_ERROR = "report-error"
    REPORT_TASK_ERROR = "report-task-error"
    SCHEMA_ERROR = "schema-error"
    FIELD_ERROR = "field-error"
    STATS_ERROR = "stats-error"

    # frictionless/errors/resource.py
    RESOURCE_ERROR = "resource-error"
    SOURCE_ERROR = "source-error"

    SCHEME_ERROR = "scheme-error"
    FORMAT_ERROR = "format-error"
    ENCODING_ERROR = "encoding-error"
    COMPRESSION_ERROR = "compression-error"

    # frictionless/errors/row.py
    ROW_ERROR = "row-error"
    BLANK_ROW = "blank-row"
    PRIMARY_KEY = "primary-key"
    FOREIGN_KEY = "foreign-key"
    DUPLICATE_ROW = "duplicate-row"
    ROW_CONSTRAINT = "row-constraint"

    # frictionless/errors/table.py
    TABLE_ERROR = "table-error"
    FIELD_COUNT = "field-count"
    ROW_COUNT = "row-count"
    TABLE_DIMENSIONS = "table-dimensions"
    DEVIATED_VALUE = "deviated-value"
    DEVIATED_CELL = "deviated-cell"
    REQUIRED_VALUE = "required-value"

    # Custom
    ONE_OF_REQUIRED = "one-of-required"
    COHESIVE_COLUMNS_VALUE = "cohesive-columns-value"
    COMPARE_COLUMNS_VALUE = "compare-columns-value"
    PHONE_NUMBER_VALUE = "phone-number-value"
    YEAR_INTERVAL_VALUE = "year-interval-value"
    OPENING_HOURS_VALUE = "opening-hours-value"
    REVERSED_FRENCH_GPS_COORDINATES = "reversed-french-gps-coordinates"
    FRENCH_GPS_COORDINATES = "french-gps-coordinates"
    NOMENCLATURE_ACTES = "nomenclature-actes"
    FRENCH_SIRET_VALUE = "french-siret-value"
    FRENCH_SIREN_VALUE = "french-siren-value"
    CUSTOM_CHECK_ERROR = "custom-check-error"
    SUM_COLUMNS_VALUE = "sum-columns-value"

    LOCAL_SOURCE_ERROR = "local-source-error"
    REMOTE_SOURCE_ERROR = "remote-source-error"
    JSON_FORMAT_ERROR = "json-format-error"

    def __repr__(self):
        return str(self)
