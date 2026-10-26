import sys

import pytest

from src.main import main
from pathlib import Path


@pytest.mark.parametrize(
    ("argument", "value"),
    [
        ("--quality", "101"),
        ("--quality", "-1"),
        ("--max-size", "0"),
        ("--thumbnail-size", "0"),
    ],
)
def test_main_rejects_invalid_numeric_arguments(
    monkeypatch: pytest.MonkeyPatch,
    argument: str,
    value: str,
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "src.main",
            "input",
            "output",
            argument,
            value,
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 2


def test_main_rejects_invalid_output_format(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "src.main",
            "input",
            "output",
            "--format",
            "gif",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 2


def test_main_exits_when_input_directory_does_not_exist(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_dir = tmp_path / "missing"
    output_dir = tmp_path / "output"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "src.main",
            str(input_dir),
            str(output_dir),
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
