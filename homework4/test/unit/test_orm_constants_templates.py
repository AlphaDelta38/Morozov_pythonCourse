from homework3.part1.orm_constants_templates import (
    create_uniques, create_varchar, create_default, create_enum
)
import pytest


def test_uniques():
    input_data = ["name", "surname"]
    result = create_uniques(input_data)
    expected = "UNIQUE(name, surname)"
    assert result == expected


@pytest.mark.parametrize("input_data, expected", [(255, 255), (1, 1), (-1, 1), (256, 255)])
def test_varchar(input_data, expected):
    result = create_varchar(input_data)
    assert result == f"VARCHAR({expected})"

@pytest.mark.parametrize("input_data, expected", [
    (["test", ["one", "two", "three"], "OR id = 1"], "CHECK (test IN (\"one\", \"two\", \"three\") OR id = 1)"),
    (["test", ["one"], ""], "CHECK (test IN (\"one\") )")
])
def test_enum(input_data, expected):
    result = create_enum(*input_data)
    assert result == expected


@pytest.mark.parametrize("input_data, expected", [("NULL", "DEFAULT NULL"), ("\"TEST\"", "DEFAULT \"TEST\"")])
def test_default(input_data, expected):
    result = create_default(input_data)
    assert result == expected
