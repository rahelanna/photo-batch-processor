import sys

import pytest

from src.main import main


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