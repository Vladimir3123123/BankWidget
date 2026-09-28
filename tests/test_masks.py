import pytest

from src.masks import get_mask_account, get_mask_card_number


class TestGetMaskCardNumber:
    """Тесты для функции get_mask_card_number."""

    def test_correct_mask(self, sample_card_number: str) -> None:
        assert get_mask_card_number(sample_card_number) == "7000 79** **** 6361"

    @pytest.mark.parametrize(
        "card_number,expected",
        [
            ("7000792289606361", "7000 79** **** 6361"),
            ("1596837868705199", "1596 83** **** 5199"),
            ("7158300734726758", "7158 30** **** 6758"),
        ],
    )
    def test_various_cards(self, card_number: str, expected: str) -> None:
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize(
        "invalid",
        [
            "",
            "123",
            "12345678901234567",  # 17 цифр
            "abcdefghijklmnop",
            "7000 7922 8960 6361",
        ],
    )
    def test_invalid_input(self, invalid: str) -> None:
        with pytest.raises(ValueError):
            get_mask_card_number(invalid)


class TestGetMaskAccount:
    """Тесты для функции get_mask_account."""

    def test_correct_mask(self, sample_account_number: str) -> None:
        assert get_mask_account(sample_account_number) == "**4305"

    @pytest.mark.parametrize(
        "account_number,expected",
        [
            ("73654108430135874305", "**4305"),
            ("64686473678894779589", "**9589"),
            ("35383033474447895560", "**5560"),
        ],
    )
    def test_various_accounts(self, account_number: str, expected: str) -> None:
        assert get_mask_account(account_number) == expected

    @pytest.mark.parametrize(
        "invalid",
        ["", "123", "1234567890123456789", "not-digits"],
    )
    def test_invalid_input(self, invalid: str) -> None:
        with pytest.raises(ValueError):
            get_mask_account(invalid)