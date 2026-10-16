import pandas as pd
import pytest

from src.csv_excel_reader import read_csv_file, read_excel_file


class TestReadCsvFile:
    """Тесты для read_csv_file."""

    def test_success(self, mocker) -> None:
        mock_df = pd.DataFrame(
            [
                {"id": 1, "amount": 100, "currency": "RUB"},
                {"id": 2, "amount": 200, "currency": "USD"},
            ]
        )
        mocker.patch("src.csv_excel_reader.pd.read_csv", return_value=mock_df)

        result = read_csv_file("fake.csv")

        assert result == [
            {"id": 1, "amount": 100, "currency": "RUB"},
            {"id": 2, "amount": 200, "currency": "USD"},
        ]

    def test_file_not_found(self, mocker) -> None:
        mocker.patch(
            "src.csv_excel_reader.pd.read_csv",
            side_effect=FileNotFoundError("no file"),
        )

        assert read_csv_file("missing.csv") == []

    def test_empty_file(self, mocker) -> None:
        mocker.patch(
            "src.csv_excel_reader.pd.read_csv",
            side_effect=pd.errors.EmptyDataError("empty"),
        )

        assert read_csv_file("empty.csv") == []

    def test_parser_error(self, mocker) -> None:
        mocker.patch(
            "src.csv_excel_reader.pd.read_csv",
            side_effect=pd.errors.ParserError("broken"),
        )

        assert read_csv_file("broken.csv") == []


class TestReadExcelFile:
    """Тесты для read_excel_file."""

    def test_success(self, mocker) -> None:
        mock_df = pd.DataFrame(
            [
                {"id": 1, "amount": 300, "currency": "EUR"},
                {"id": 2, "amount": 400, "currency": "RUB"},
            ]
        )
        mocker.patch("src.csv_excel_reader.pd.read_excel", return_value=mock_df)

        result = read_excel_file("fake.xlsx")

        assert result == [
            {"id": 1, "amount": 300, "currency": "EUR"},
            {"id": 2, "amount": 400, "currency": "RUB"},
        ]

    def test_file_not_found(self, mocker) -> None:
        mocker.patch(
            "src.csv_excel_reader.pd.read_excel",
            side_effect=FileNotFoundError("no file"),
        )

        assert read_excel_file("missing.xlsx") == []

    def test_value_error(self, mocker) -> None:
        mocker.patch(
            "src.csv_excel_reader.pd.read_excel",
            side_effect=ValueError("bad excel"),
        )

        assert read_excel_file("broken.xlsx") == []

    def test_reads_real_csv(self) -> None:
        """Дополнительный тест: реальный CSV (если есть)."""
        try:
            result = read_csv_file("data/transactions.csv")
            assert isinstance(result, list)
        except FileNotFoundError:
            pytest.skip("data/transactions.csv отсутствует")
