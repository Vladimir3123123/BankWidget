import pytest

from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для функции filter_by_state."""

    def test_default_state(self, sample_operations: list[dict]) -> None:
        result = filter_by_state(sample_operations)
        assert len(result) == 2
        assert all(item["state"] == "EXECUTED" for item in result)

    @pytest.mark.parametrize("state", ["EXECUTED", "CANCELED"])
    def test_various_states(self, sample_operations: list[dict], state: str) -> None:
        result = filter_by_state(sample_operations, state)
        assert all(item["state"] == state for item in result)

    def test_no_matches(self, sample_operations: list[dict]) -> None:
        assert filter_by_state(sample_operations, "PENDING") == []

    def test_empty_list(self, empty_operations: list[dict]) -> None:
        assert filter_by_state(empty_operations) == []


class TestSortByDate:
    """Тесты для функции sort_by_date."""

    def test_default_desc(self, sample_operations: list[dict]) -> None:
        result = sort_by_date(sample_operations)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates, reverse=True)

    def test_asc(self, sample_operations: list[dict]) -> None:
        result = sort_by_date(sample_operations, reverse=False)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates)

    def test_same_dates(self) -> None:
        data = [
            {"id": 1, "date": "2024-01-01T00:00:00"},
            {"id": 2, "date": "2024-01-01T00:00:00"},
        ]
        result = sort_by_date(data)
        assert len(result) == 2

    def test_empty(self, empty_operations: list[dict]) -> None:
        assert sort_by_date(empty_operations) == []