import pytest

from src import external_api


class TestConvertToRub:
    """Тесты для функции convert_to_rub."""

    def test_rub_transaction_no_api_call(self, mocker) -> None:
        """RUB — без обращения к API."""
        mock_get = mocker.patch("src.external_api.requests.get")

        transaction = {
            "operationAmount": {
                "amount": "1000.50",
                "currency": {"name": "руб.", "code": "RUB"},
            }
        }
        result = external_api.convert_to_rub(transaction)

        assert result == 1000.50
        mock_get.assert_not_called()

    def test_usd_transaction_calls_api(self, mocker) -> None:
        """USD — обращается к API, возвращает конвертированную сумму."""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"result": 750000.0}
        mock_response.raise_for_status = mocker.Mock()

        mock_get = mocker.patch(
            "src.external_api.requests.get", return_value=mock_response
        )

        transaction = {
            "operationAmount": {
                "amount": "10000",
                "currency": {"name": "USD", "code": "USD"},
            }
        }
        result = external_api.convert_to_rub(transaction)

        assert result == 750000.0
        mock_get.assert_called_once()

    def test_eur_transaction_calls_api(self, mocker) -> None:
        """EUR — обращается к API."""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"result": 800000.0}
        mock_response.raise_for_status = mocker.Mock()

        mocker.patch("src.external_api.requests.get", return_value=mock_response)

        transaction = {
            "operationAmount": {
                "amount": "10000",
                "currency": {"name": "EUR", "code": "EUR"},
            }
        }
        result = external_api.convert_to_rub(transaction)

        assert result == 800000.0

    def test_unsupported_currency(self) -> None:
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"name": "Yen", "code": "JPY"},
            }
        }
        with pytest.raises(ValueError, match="Неподдерживаемая валюта"):
            external_api.convert_to_rub(transaction)

    def test_missing_api_key(self, mocker) -> None:
        mocker.patch("src.external_api.API_KEY", None)

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"name": "USD", "code": "USD"},
            }
        }
        with pytest.raises(ValueError, match="EXCHANGE_RATES_API_KEY"):
            external_api.convert_to_rub(transaction)

    def test_api_error_status(self, mocker) -> None:
        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 401")

        mocker.patch("src.external_api.requests.get", return_value=mock_response)

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"name": "USD", "code": "USD"},
            }
        }
        with pytest.raises(Exception, match="HTTP 401"):
            external_api.convert_to_rub(transaction)