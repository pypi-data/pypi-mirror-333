from typing import Optional

from .error_types import ErrType
from .metadata import Metadata, metadata_or_default


class TypedException(Exception):
    type: ErrType
    metadata: Metadata

    def __init__(
        self, message: str, type: ErrType, metadata: Optional[Metadata] = None
    ):
        super().__init__(message)
        self.type = type
        self.metadata = metadata_or_default(metadata)

    @classmethod
    def new(cls, type: ErrType, note: str = "") -> "TypedException":
        message = cls.message_for_type(type)
        if note:
            message += " ; " + note
        return cls(message, type)

    @staticmethod
    def message_for_type(type: ErrType) -> str:
        if type == ErrType.FORMAT_ERROR:
            return "Format non supporté ou invalide"
        if type == ErrType.JSON_FORMAT_ERROR:
            return "JSON non valide"

        if type == ErrType.SOURCE_ERROR:
            return "Erreur de lecture des données"
        if type == ErrType.REMOTE_SOURCE_ERROR:
            return "Erreur de lecture de données distantes"
        if type == ErrType.LOCAL_SOURCE_ERROR:
            return "Erreur de lecture de données locales"
        return ""
