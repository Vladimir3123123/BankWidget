import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCard:
    """Тесты для функции mask_account_card."""

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
            ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
            ("Счет 73654108430135874305", "Счет **4305"),
            ("Счет 64686473678894779589", "Счет **9589"),
        ],
    )
    def test_valid(self, value: str, expected: str) -> None:
        assert mask_account_card(value) == expected

    @pytest.mark.parametrize("invalid", ["", "   ", "Visa", "Visa Platinum"])
    def test_invalid(self, invalid: str) -> None:
        with pytest.raises(ValueError):
            mask_account_card(invalid)


class TestGetDate:
    """Тесты для функции get_date."""

    def test_correct(self, sample_iso_date: str) -> None:
        assert get_date(sample_iso_date) == "11.03.2024"

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024"),
            ("2019-07-03T18:35:29.512364", "03.07.2019"),
            ("2018-06-30T02:08:58.425572", "30.06.2018"),
        ],
    )
    def test_various_dates(self, value: str, expected: str) -> None:
        assert get_date(value) == expected

    def test_empty(self) -> None:
        with pytest.raises(ValueError):
            get_date("")