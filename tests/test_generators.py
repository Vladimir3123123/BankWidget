import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


class TestFilterByCurrency:
    """Тесты для filter_by_currency."""

    def test_returns_iterator(self, sample_transactions: list[dict]) -> None:
        result = filter_by_currency(sample_transactions, "USD")
        assert hasattr(result, "__next__")

    @pytest.mark.parametrize(
        "currency,expected_count",
        [
            ("USD", 3),
            ("RUB", 1),
            ("EUR", 0),
        ],
    )
    def test_filter_by_currency(
        self, sample_transactions: list[dict], currency: str, expected_count: int
    ) -> None:
        result = list(filter_by_currency(sample_transactions, currency))
        assert len(result) == expected_count

    def test_usd_transactions_have_correct_code(
        self, sample_transactions: list[dict]
    ) -> None:
        result = list(filter_by_currency(sample_transactions, "USD"))
        for item in result:
            assert item["operationAmount"]["currency"]["code"] == "USD"

    def test_empty_list(self, empty_transactions: list[dict]) -> None:
        result = list(filter_by_currency(empty_transactions, "USD"))
        assert result == []


class TestTransactionDescriptions:
    """Тесты для transaction_descriptions."""

    def test_returns_generator(self, sample_transactions: list[dict]) -> None:
        result = transaction_descriptions(sample_transactions)
        assert hasattr(result, "__next__")

    def test_descriptions(self, sample_transactions: list[dict]) -> None:
        result = list(transaction_descriptions(sample_transactions))
        assert result == [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
        ]

    def test_empty_list(self, empty_transactions: list[dict]) -> None:
        assert list(transaction_descriptions(empty_transactions)) == []

    def test_first_five(self, sample_transactions: list[dict]) -> None:
        gen = transaction_descriptions(sample_transactions)
        first = next(gen)
        assert first == "Перевод организации"


class TestCardNumberGenerator:
    """Тесты для card_number_generator."""

    def test_returns_generator(self) -> None:
        result = card_number_generator(1, 5)
        assert hasattr(result, "__next__")

    def test_first_five(self) -> None:
        result = list(card_number_generator(1, 5))
        assert result == [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]

    @pytest.mark.parametrize(
        "start,stop,expected_first,expected_last,expected_len",
        [
            (1, 1, "0000 0000 0000 0001", "0000 0000 0000 0001", 1),
            (100, 102, "0000 0000 0000 0100", "0000 0000 0000 0102", 3),
            (
                9999999999999998,
                9999999999999999,
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
                2,
            ),
        ],
    )
    def test_ranges(
        self,
        start: int,
        stop: int,
        expected_first: str,
        expected_last: str,
        expected_len: int,
    ) -> None:
        result = list(card_number_generator(start, stop))
        assert len(result) == expected_len
        assert result[0] == expected_first
        assert result[-1] == expected_last

    def test_format(self) -> None:
        for card in card_number_generator(1, 10):
            parts = card.split(" ")
            assert len(parts) == 4
            assert all(len(part) == 4 and part.isdigit() for part in parts)

    def test_empty_range(self) -> None:
        assert list(card_number_generator(5, 4)) == []