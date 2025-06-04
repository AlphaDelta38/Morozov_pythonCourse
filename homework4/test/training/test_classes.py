from homework4.test.training.clases import DataProcessor
from unittest.mock import patch
import pytest


@pytest.fixture()
def obj():
    return DataProcessor()


def test_process_data(obj):
    input_data = [4, 6]
    result = obj.process_data(input_data)
    expected = [8, 12]
    assert result == expected


@patch.object(DataProcessor, 'process_data', return_value=[8, 12])
def test_analyze_data(mock_fn, obj):
    input_data = [4, 6]
    result = obj.analyze_data(input_data)
    expected = 20
    assert result == expected
