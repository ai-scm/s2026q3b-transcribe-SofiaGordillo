"""Configuración de la aplicación."""

from dataclasses import dataclass


DEFAULT_LANGUAGE = "es"
DEFAULT_MODEL = "small"
DEFAULT_DEVICE = "cpu"
DEFAULT_COMPUTE_TYPE = "int8"


@dataclass(frozen=True)
class TranscriptionConfig:
    """Configuración utilizada para una transcripción."""

    language: str = DEFAULT_LANGUAGE
    model: str = DEFAULT_MODEL
    device: str = DEFAULT_DEVICE
    compute_type: str = DEFAULT_COMPUTE_TYPE
