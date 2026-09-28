import pytest


@pytest.fixture
def sample_operations() -> list[dict]:
    """Список операций с разными статусами и датами для тестов."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def empty_operations() -> list[dict]:
    """Пустой список операций."""
    return []


@pytest.fixture
def sample_card_number() -> str:
    """Корректный номер карты (16 цифр)."""
    return "7000792289606361"


@pytest.fixture
def sample_account_number() -> str:
    """Корректный номер счёта (20 цифр)."""
    return "73654108430135874305"


@pytest.fixture
def sample_iso_date() -> str:
    """Корректная ISO-дата."""
    return "2024-03-11T02:26:18.671407"