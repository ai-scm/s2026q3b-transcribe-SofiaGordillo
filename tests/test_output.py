from pathlib import Path

import pytest

from transcriber.output import (
    create_output_file,
    format_timestamp,
    write_segment,
)


def test_format_timestamp() -> None:
    assert format_timestamp(0) == "00:00:00,000"
    assert format_timestamp(65.432) == "00:01:05,432"
    assert format_timestamp(3661.5) == "01:01:01,500"


def test_format_timestamp_negative() -> None:
    with pytest.raises(ValueError):
        format_timestamp(-1)


def test_write_segment(tmp_path: Path) -> None:
    output_file = tmp_path / "test.sub"

    with create_output_file(output_file) as file:
        write_segment(
            file=file,
            index=1,
            start=0.0,
            end=3.5,
            text="Hola, esta es una prueba.",
        )

    content = output_file.read_text(encoding="utf-8")

    assert "1" in content
    assert "00:00:00,000 --> 00:00:03,500" in content
    assert "Hola, esta es una prueba." in content


def test_write_empty_segment(tmp_path: Path) -> None:
    output_file = tmp_path / "test.sub"

    with create_output_file(output_file) as file:
        write_segment(
            file=file,
            index=1,
            start=0.0,
            end=2.0,
            text="   ",
        )

    content = output_file.read_text(encoding="utf-8")

    assert content == ""


def test_write_invalid_timestamps(tmp_path: Path) -> None:
    output_file = tmp_path / "test.sub"

    with create_output_file(output_file) as file:
        with pytest.raises(ValueError):
            write_segment(
                file=file,
                index=1,
                start=5.0,
                end=2.0,
                text="Texto inválido.",
            )
