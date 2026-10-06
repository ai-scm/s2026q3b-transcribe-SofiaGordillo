"""Validaciones de archivos de entrada y salida."""

from pathlib import Path


SUPPORTED_EXTENSIONS = {".mp3", ".mp4"}


class ValidationError(Exception):
    """Error producido cuando un archivo no cumple los requisitos."""


def validate_input_file(file_path: Path) -> Path:
    """Valida que el archivo exista, sea legible y tenga un formato soportado."""

    file_path = file_path.expanduser().resolve()

    if not file_path.exists():
        raise ValidationError(
            f"El archivo no existe: {file_path}"
        )

    if not file_path.is_file():
        raise ValidationError(
            f"La ruta no corresponde a un archivo: {file_path}"
        )

    if not file_path.stat().st_mode & 0o444:
        raise ValidationError(
            f"El archivo no tiene permisos de lectura: {file_path}"
        )

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValidationError(
            f"Formato no soportado: {file_path.suffix}. "
            f"Formatos permitidos: {supported}"
        )

    return file_path


def get_output_path(input_path: Path) -> Path:
    """Obtiene la ruta del archivo .sub correspondiente al archivo de entrada."""

    return input_path.with_suffix(".sub")


def validate_output_path(output_path: Path, force: bool = False) -> None:
    """Valida si se puede crear o reemplazar el archivo de salida."""

    if output_path.exists() and not force:
        raise ValidationError(
            f"El archivo de salida ya existe: {output_path}"
        )
