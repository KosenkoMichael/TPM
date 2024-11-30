import json

import pytest

from unittest.mock import patch, mock_open

from algoritms.functional import Functional

@pytest.mark.parametrize(
    "mock_data, expected_result", [
        ('{"key1": "value1", "key2": "value2"}', {"key1": "value1", "key2": "value2"}),
        ('{"name": "John", "age": 30, "city": "New York"}', {"name": "John", "age": 30, "city": "New York"}),
        ('{}', {}),  # Empty JSON object
        ('{"valid": true, "empty_array": []}', {"valid": True, "empty_array": []}), 
        ('{"error": "invalid"}', {"error": "invalid"}),
    ]
)
@patch("builtins.open", new_callable=mock_open)
@patch("json.load") 
def test_read_json(mock_json_load, mock_file, mock_data, expected_result):
    """Test read_json with parameterized inputs and mocked file I/O"""

    mock_json_load.return_value = json.loads(mock_data)

    result = Functional.read_json("fake_path.json")

    mock_file.assert_called_once_with("fake_path.json", "r", encoding="UTF-8")

    mock_json_load.assert_called_once_with(mock_file())

    assert result == expected_result, f"Expected {expected_result}, but got {result}"


@pytest.mark.parametrize(
    "file_path, data, expected_result",
    [
        ("test_file_1.txt", "Hello, world!", "Hello, world!"),
        ("test_file_2.txt", "Test data", "Test data"),
        ("test_file_3.txt", "", ""),
    ]
)
@patch("builtins.open", new_callable=mock_open)
def test_write_file(mock_file, file_path, data, expected_result):
    Functional.write_file(file_path, data)
    mock_file.assert_called_once_with(file_path, "w", encoding="utf-8")
    mock_file().write.assert_called_once_with(expected_result)


@patch("builtins.open", side_effect=OSError("File system error"))
def test_write_file_error(mock_open):
    Functional.write_file("test_file_error.txt", "Some data")
    mock_open.assert_called_once_with("test_file_error.txt", "w", encoding="utf-8")
    assert mock_open.call_count == 1
