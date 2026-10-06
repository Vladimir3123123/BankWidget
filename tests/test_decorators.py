import os

import pytest

from src.decorators import log


class TestLogToConsole:
    """Тесты для декоратора log с выводом в консоль."""

    def test_success_prints_ok(self, capsys: pytest.CaptureFixture) -> None:
        @log()
        def add(x: int, y: int) -> int:
            return x + y

        result = add(1, 2)

        captured = capsys.readouterr()
        assert result == 3
        assert "add ok" in captured.out

    def test_error_prints_message(self, capsys: pytest.CaptureFixture) -> None:
        @log()
        def divide(x: int, y: int) -> float:
            return x / y

        with pytest.raises(ZeroDivisionError):
            divide(1, 0)

        captured = capsys.readouterr()
        assert "divide error" in captured.out
        assert "ZeroDivisionError" in captured.out
        assert "(1, 0)" in captured.out

    def test_error_with_kwargs(self, capsys: pytest.CaptureFixture) -> None:
        @log()
        def divide(x: int, y: int) -> float:
            return x / y

        with pytest.raises(ZeroDivisionError):
            divide(x=1, y=0)

        captured = capsys.readouterr()
        assert "divide error" in captured.out
        assert "ZeroDivisionError" in captured.out
        assert "{'x': 1, 'y': 0}" in captured.out


class TestLogToFile:
    """Тесты для декоратора log с записью в файл."""

    def test_success_writes_ok(self, tmp_path) -> None:
        log_file = tmp_path / "mylog.txt"

        @log(filename=str(log_file))
        def add(x: int, y: int) -> int:
            return x + y

        add(1, 2)

        content = log_file.read_text(encoding="utf-8")
        assert "add ok" in content

    def test_error_writes_message(self, tmp_path) -> None:
        log_file = tmp_path / "mylog.txt"

        @log(filename=str(log_file))
        def divide(x: int, y: int) -> float:
            return x / y

        with pytest.raises(ZeroDivisionError):
            divide(1, 0)

        content = log_file.read_text(encoding="utf-8")
        assert "divide error" in content
        assert "ZeroDivisionError" in content
        assert "(1, 0)" in content

    def test_file_appends(self, tmp_path) -> None:
        log_file = tmp_path / "mylog.txt"

        @log(filename=str(log_file))
        def add(x: int, y: int) -> int:
            return x + y

        add(1, 2)
        add(3, 4)

        content = log_file.read_text(encoding="utf-8")
        assert content.count("add ok") == 2

    def test_no_console_output_when_file_set(
        self, tmp_path, capsys: pytest.CaptureFixture
    ) -> None:
        log_file = tmp_path / "mylog.txt"

        @log(filename=str(log_file))
        def add(x: int, y: int) -> int:
            return x + y

        add(1, 2)

        captured = capsys.readouterr()
        assert captured.out == ""


class TestLogPreservesMetadata:
    """Проверяет, что декоратор сохраняет метаданные функции."""

    def test_function_name_preserved(self) -> None:
        @log()
        def my_function() -> None:
            """Docstring."""
            return None

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "Docstring."