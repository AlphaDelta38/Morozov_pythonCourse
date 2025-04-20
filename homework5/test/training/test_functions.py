from homework5.test.training.functions import (
    process_mock_object,
    run_data_pipeline,
    check_even_odd,
    divide_numbers,
    add_numbers,
    fetch_data,
    is_even
)
from unittest.mock import MagicMock, call, patch
import pytest


JSON_PLACEHOLDER_POST_URL = "https://jsonplaceholder.typicode.com/posts"


def test_add_numbers():
    input_data = [1, 2]
    result = add_numbers(*input_data)
    assert result == 3


@pytest.mark.parametrize("input_data, expected", [(2, True), (3, False)])
def test_is_even(input_data, expected):
    result = is_even(input_data)
    assert result == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [(JSON_PLACEHOLDER_POST_URL, True), (f"{JSON_PLACEHOLDER_POST_URL}/dd", False)]
    )
def test_fetch_data(input_data, expected):
    result = fetch_data(input_data)
    if expected:
        assert result is not None
    else:
        assert result is None


def test_process_mock_object_raises_nameerror():
    mock = MagicMock()
    mock.value = 1
    with pytest.raises(NameError):
        process_mock_object(mock)


def test_process_mock_object_returns_none():
    mock = MagicMock()
    mock.value = 0
    result = process_mock_object(mock)
    assert result is None


def test_run_data_pipeline():
    mock = MagicMock()
    run_data_pipeline(mock)
    expected = [call.process_data(),call.process_data().analyze_data(),call.process_data().analyze_data().save_result()]

    assert expected == mock.mock_calls


@pytest.mark.parametrize("input_data, expected", [([4, 2], 2), ([0, 4], 0), ([4, 0], None)])
def test_divide_numbers(input_data, expected):
    result = divide_numbers(*input_data)
    assert result == expected


@patch("homework5.test.training.functions.requests.get")
def test_check_even_odd(mock_req):
    mock_response_1 = MagicMock()
    mock_response_1.json.return_value = {"results": [{"value": 2}]}

    mock_response_2 = MagicMock()
    mock_response_2.json.return_value = {"results": [{"value": 3}]}

    mock_req.side_effect = [mock_response_1, mock_response_2]

    result = check_even_odd([0, 0], "")
    expected = ["Even", "Odd"]

    assert result == expected





