"""Interfaz de línea de comandos para la transcripción."""

import argparse
import sys
from pathlib import Path

from .config import (
    DEFAULT_LANGUAGE,
    DEFAULT_MODEL,
    TranscriptionConfig,
)
from .output import create_output_file, write_segment
from .transcriber import Transcriber, TranscriptionError
from .validation import (
    ValidationError,
    get_output_path,
    validate_input_file,
    validate_output_path,
)


def parse_arguments() -> argparse.Namespace:
    """Procesa los argumentos de la línea de comandos."""

    parser = argparse.ArgumentParser(
        prog="transcribir",
        description=(
            "Transcribe archivos MP3 y MP4 utilizando "
            "faster-whisper."
        ),
    )

    parser.add_argument(
        "file",
        type=Path,
        help="Archivo MP3 o MP4 que se desea transcribir.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Sobrescribe el archivo .sub existente sin preguntar.",
    )

    parser.add_argument(
        "--language",
        default=DEFAULT_LANGUAGE,
        help=(
            f"Idioma de la transcripción. "
            f"Predeterminado: {DEFAULT_LANGUAGE}"
        ),
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Modelo Whisper. Predeterminado: {DEFAULT_MODEL}",
    )

    return parser.parse_args()


def confirm_overwrite(output_path: Path) -> bool:
    """Solicita confirmación antes de sobrescribir un archivo."""

    try:
        answer = input(
            f"El archivo {output_path} ya existe. "
            "¿Desea sobrescribirlo? [s/N]: "
        )
    except EOFError:
        return False

    return answer.strip().lower() in {"s", "si", "sí", "y", "yes"}


def transcribe_file(
    input_path: Path,
    output_path: Path,
    config: TranscriptionConfig,
) -> int:
    """Realiza la transcripción y genera el archivo .sub."""

    print(f"Archivo de entrada: {input_path}")
    print(f"Archivo de salida: {output_path}")
    print(f"Modelo: {config.model}")
    print(f"Idioma: {config.language}")
    print("Iniciando transcripción...")

    transcriber = Transcriber(config)

    segment_count = 0
    previous_start = 0.0

    temporary_path = output_path.with_suffix(".sub.tmp")

    try:
        with create_output_file(temporary_path) as output_file:
            for index, segment in enumerate(
                transcriber.transcribe(str(input_path)),
                start=1,
            ):
                if segment.start < 0 or segment.end < 0:
                    raise TranscriptionError(
                        "Se recibió un timestamp negativo."
                    )

                if segment.end < segment.start:
                    raise TranscriptionError(
                        "Se recibió un segmento con timestamps inválidos."
                    )

                if segment_count > 0 and segment.start < previous_start:
                    raise TranscriptionError(
                        "Los timestamps iniciales de los segmentos "
                        "no están ordenados."
                    )

                write_segment(
                    output_file,
                    index,
                    segment.start,
                    segment.end,
                    segment.text,
                )

                previous_start = segment.start
                segment_count += 1

                print(
                    f"\rSegmentos procesados: {segment_count}",
                    end="",
                    flush=True,
                )

        print()

        if segment_count == 0:
            raise TranscriptionError(
                "La transcripción no produjo ningún segmento de texto."
            )

        temporary_path.replace(output_path)

    except Exception:
        if temporary_path.exists():
            temporary_path.unlink()
        raise

    print(
        f"Transcripción completada. "
        f"{segment_count} segmentos escritos."
    )

    return 0


def main() -> int:
    """Punto de entrada principal del comando transcribir."""

    args = parse_arguments()

    try:
        input_path = validate_input_file(args.file)
        output_path = get_output_path(input_path)

        if output_path.exists() and not args.force:
            if not confirm_overwrite(output_path):
                print("Operación cancelada.")
                return 1

        validate_output_path(output_path, force=args.force)

        config = TranscriptionConfig(
            language=args.language,
            model=args.model,
        )

        return transcribe_file(
            input_path,
            output_path,
            config,
        )

    except ValidationError as exc:
        print(f"Error de validación: {exc}", file=sys.stderr)
        return 2

    except TranscriptionError as exc:
        print(f"Error de transcripción: {exc}", file=sys.stderr)
        return 3

    except KeyboardInterrupt:
        print("\nTranscripción cancelada.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
