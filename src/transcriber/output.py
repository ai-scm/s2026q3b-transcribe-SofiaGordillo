"""Generación de archivos de subtítulos .sub."""

from pathlib import Path
from typing import TextIO


def format_timestamp(seconds: float) -> str:
    """Convierte segundos a formato HH:MM:SS,mmm."""

    if seconds < 0:
        raise ValueError("El timestamp no puede ser negativo.")

    total_milliseconds = round(seconds * 1000)

    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds_value, milliseconds = divmod(remainder, 1_000)

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{seconds_value:02d},"
        f"{milliseconds:03d}"
    )


def write_segment(
    file: TextIO,
    index: int,
    start: float,
    end: float,
    text: str,
) -> None:
    """Escribe un segmento en formato SRT dentro del archivo .sub."""

    if start < 0:
        raise ValueError("El timestamp inicial no puede ser negativo.")

    if end < 0:
        raise ValueError("El timestamp final no puede ser negativo.")

    if end < start:
        raise ValueError(
            "El timestamp final no puede ser menor al inicial."
        )

    if not text.strip():
        return

    file.write(f"{index}\n")
    file.write(
        f"{format_timestamp(start)} --> {format_timestamp(end)}\n"
    )
    file.write(f"{text.strip()}\n\n")


def create_output_file(output_path: Path) -> TextIO:
    """Crea el archivo de salida para escribir la transcripción."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    return output_path.open(
        mode="w",
        encoding="utf-8",
        newline="\n",
    )
