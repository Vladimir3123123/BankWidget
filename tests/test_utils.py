import json

import pytest

from src.utils import load_transactions


class TestLoadTransactions:
    """Тесты для функции load_transactions."""

    def test_valid_file(self, tmp_path) -> None:
        data = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "CANCELED"},
        ]
        file = tmp_path / "operations.json"
        file.write_text(json.dumps(data), encoding="utf-8")

        result = load_transactions(str(file))
        assert result == data

    def test_empty_file(self, tmp_path) -> None:
        file = tmp_path / "empty.json"
        file.write_text("", encoding="utf-8")

        assert load_transactions(str(file)) == []

    def test_not_a_list(self, tmp_path) -> None:
        file = tmp_path / "dict.json"
        file.write_text(json.dumps({"key": "value"}), encoding="utf-8")

        assert load_transactions(str(file)) == []

    def test_invalid_json(self, tmp_path) -> None:
        file = tmp_path / "broken.json"
        file.write_text("{not valid json", encoding="utf-8")

        assert load_transactions(str(file)) == []

    def test_file_not_found(self) -> None:
        assert load_transactions("nonexistent_file.json") == []

    def test_real_operations_file(self) -> None:
        result = load_transactions("data/operations.json")
        assert isinstance(result, list)