from src.processing import process_bank_operations, process_bank_search


class TestProcessBankSearch:
    """Тесты для process_bank_search."""

    @pytest.fixture
    def sample_data(self) -> list[dict]:
        return [
            {"description": "Перевод организации", "state": "EXECUTED"},
            {"description": "Перевод со счета на счет", "state": "EXECUTED"},
            {"description": "Открытие вклада", "state": "EXECUTED"},
            {"description": "Перевод с карты на карту", "state": "CANCELED"},
        ]

    def test_search_by_word(self, sample_data: list[dict]) -> None:
        result = process_bank_search(sample_data, "Перевод")
        assert len(result) == 3

    def test_search_case_insensitive(self, sample_data: list[dict]) -> None:
        result = process_bank_search(sample_data, "перевод")
        assert len(result) == 3

    def test_search_no_matches(self, sample_data: list[dict]) -> None:
        result = process_bank_search(sample_data, "xyz")
        assert result == []

    def test_search_empty_string(self, sample_data: list[dict]) -> None:
        result = process_bank_search(sample_data, "")
        assert len(result) == len(sample_data)

    def test_search_special_chars(self, sample_data: list[dict]) -> None:
        """re.escape защищает от regex-спецсимволов."""
        result = process_bank_search(sample_data, ".*")
        assert result == []


class TestProcessBankOperations:
    """Тесты для process_bank_operations."""

    @pytest.fixture
    def sample_data(self) -> list[dict]:
        return [
            {"description": "Перевод организации"},
            {"description": "Перевод организации"},
            {"description": "Перевод со счета на счет"},
            {"description": "Открытие вклада"},
        ]

    def test_counts_correctly(self, sample_data: list[dict]) -> None:
        result = process_bank_operations(sample_data, ["Перевод организации", "Открытие вклада"])
        assert result == {"Перевод организации": 2, "Открытие вклада": 1}

    def test_zero_for_absent_category(self, sample_data: list[dict]) -> None:
        result = process_bank_operations(sample_data, ["Несуществующая"])
        assert result == {"Несуществующая": 0}

    def test_empty_data(self) -> None:
        result = process_bank_operations([], ["Перевод организации"])
        assert result == {"Перевод организации": 0}

    def test_case_insensitive(self, sample_data: list[dict]) -> None:
        result = process_bank_operations(sample_data, ["перевод организации"])
        assert result == {"перевод организации": 2}
