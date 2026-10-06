"""Motor de transcripción utilizando faster-whisper."""

from collections.abc import Iterator
from dataclasses import dataclass

from faster_whisper import WhisperModel

from .config import TranscriptionConfig


@dataclass(frozen=True)
class TranscriptionSegment:
    """Segmento de texto transcrito con sus timestamps."""

    start: float
    end: float
    text: str


class TranscriptionError(Exception):
    """Error producido durante la transcripción."""


class Transcriber:
    """Encapsula el modelo faster-whisper."""

    def __init__(self, config: TranscriptionConfig) -> None:
        self.config = config

        try:
            self.model = WhisperModel(
                config.model,
                device=config.device,
                compute_type=config.compute_type,
            )
        except Exception as exc:
            raise TranscriptionError(
                f"No fue posible cargar el modelo Whisper: {exc}"
            ) from exc

    def transcribe(
        self,
        audio_path: str,
    ) -> Iterator[TranscriptionSegment]:
        """Transcribe el archivo y devuelve segmentos progresivamente."""

        try:
            segments, _info = self.model.transcribe(
                audio_path,
                language=self.config.language,
                vad_filter=False,
            )

            for segment in segments:
                text = segment.text.strip()

                if not text:
                    continue

                yield TranscriptionSegment(
                    start=float(segment.start),
                    end=float(segment.end),
                    text=text,
                )

        except Exception as exc:
            raise TranscriptionError(
                f"Error durante la transcripción: {exc}"
            ) from exc
