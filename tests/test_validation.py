from pathlib import Path

import pytest

from transcriber.validation import (
    ValidationError,
    get_output_path,
    validate_input_file,
    validate_output_path,
)


def test_validate_supported_mp3(tmp_path: Path) -> None:
    audio_file = tmp_path / "audio.mp3"
    audio_file.write_bytes(b"fake mp3 content")

    result = validate_input_file(audio_file)

    assert result == audio_file.resolve()


def test_validate_supported_mp4(tmp_path: Path) -> None:
    video_file = tmp_path / "video.mp4"
    video_file.write_bytes(b"fake mp4 content")

    result = validate_input_file(video_file)

    assert result == video_file.resolve()


def test_missing_file() -> None:
    with pytest.raises(ValidationError):
        validate_input_file(Path("/tmp/no-existe.mp3"))


def test_unsupported_extension(tmp_path: Path) -> None:
    text_file = tmp_path / "document.txt"
    text_file.write_text("texto")

    with pytest.raises(ValidationError):
        validate_input_file(text_file)


def test_output_path(tmp_path: Path) -> None:
    input_file = tmp_path / "reunion.mp4"

    output_file = get_output_path(input_file)

    assert output_file == tmp_path / "reunion.sub"


def test_existing_output_without_force(tmp_path: Path) -> None:
    output_file = tmp_path / "reunion.sub"
    output_file.write_text("contenido anterior")

    with pytest.raises(ValidationError):
        validate_output_path(output_file, force=False)


def test_existing_output_with_force(tmp_path: Path) -> None:
    output_file = tmp_path / "reunion.sub"
    output_file.write_text("contenido anterior")

    validate_output_path(output_file, force=True)
