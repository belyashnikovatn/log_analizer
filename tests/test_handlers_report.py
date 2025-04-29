import pytest
from log_analyzer.parser import parse_log_line, parse_log_file
from log_analyzer.reports.handlers import (
    generate_handlers_report,
    merge_reports,
    format_handlers_report,
)
from log_analyzer.models import ReportData
from log_analyzer.utils import validate_file_paths

from main import process_files


def test_validate_file_paths_all_exist(tmp_path):
    """Проверяет, что все файлы существуют."""
    file1 = tmp_path / "log1.txt"
    file2 = tmp_path / "log2.txt"
    file1.write_text("log entry 1")
    file2.write_text("log entry 2")

    result = validate_file_paths([str(file1), str(file2)])
    assert result is True


def test_validate_file_paths_some_missing(tmp_path):
    """Проверяет, что функция возвращает False, если хотя бы один файл отсутствует."""
    file1 = tmp_path / "exists.log"
    file1.write_text("log entry")
    missing_file = tmp_path / "missing.log"

    result = validate_file_paths([str(file1), str(missing_file)])
    assert result is False


def test_parse_valid_log_line():
    """Проверяет, что валидная строка лога парсится корректно."""
    line = "2025-04-29 10:00:00,000 INFO django.request: GET /home 200 OK"
    entry = parse_log_line(line)
    assert entry is not None
    assert entry.timestamp == "2025-04-29 10:00:00,000"
    assert entry.level == "INFO"
    assert entry.handler == "/home"
    assert "GET /home 200 OK" in entry.message


def test_parse_invalid_log_line():
    """Проверяет, что невалидная строка лога возвращает None."""
    line = "INVALID LOG LINE"
    entry = parse_log_line(line)
    assert entry is None


def test_parse_log_line_not_request_logger():
    """Проверяет, что строка с другим логгером парсится корректно."""
    line = "2025-04-29 10:00:00,000 INFO other.logger: Some message"
    entry = parse_log_line(line)
    assert entry is not None
    assert entry.handler is None


def test_parse_log_file(tmp_path):
    """Проверяет, что файл лога парсится корректно."""
    file = tmp_path / "test.log"
    file.write_text(
        "2025-04-29 10:00:00,000 INFO django.request: GET /home 200 OK\n"
        "invalid line\n"
        "2025-04-29 10:01:00,000 ERROR django.request: GET /error 500 Internal Server Error\n"
    )
    entries = list(parse_log_file(str(file)))
    assert len(entries) == 2
    assert entries[0].handler == "/home"
    assert entries[1].handler == "/error"


def test_generate_report_from_empty_list():
    """Проверяет, что генерация отчета из пустого списка возвращает пустой отчет."""
    report = generate_handlers_report([])
    assert report.total == 0
    assert report.handlers == {}


def test_merge_reports_with_different_handlers():
    """Проверяет, что слияние отчётов с разными обработчиками работает корректно."""
    report1 = ReportData(handlers={"/a": {"INFO": 2}}, total=2)
    report2 = ReportData(handlers={"/b": {"ERROR": 3}}, total=3)
    merged = merge_reports([report1, report2])
    assert merged.total == 5
    assert merged.handlers["/a"]["INFO"] == 2
    assert merged.handlers["/b"]["ERROR"] == 3


def test_format_empty_report():
    """Проверяет, что форматирование пустого отчёта возвращает сообщение о том, что нет данных."""
    report = ReportData(handlers={}, total=0)
    formatted = format_handlers_report(report)
    assert "No data to display" in formatted


def test_format_nonempty_report():
    """Проверяет, что форматирование непустого отчёта работает корректно."""
    report = ReportData(handlers={"/home": {"INFO": 1, "ERROR": 2}}, total=3)
    output = format_handlers_report(report)
    assert "Total requests: 3" in output
    assert "/home" in output
    assert "INFO" in output
    assert "ERROR" in output


def test_process_files_full_cycle(tmp_path):
    """Проверяет полный цикл обработки файлов и генерации отчета."""
    file = tmp_path / "access.log"
    file.write_text(
        "2025-04-29 10:00:00,000 INFO django.request: GET /index 200 OK\n"
        "2025-04-29 10:00:01,000 ERROR django.request: GET /index 500 Internal Error\n"
    )
    result = process_files([str(file)], "handlers")
    assert "Total requests: 2" in result
    assert "/index" in result
    assert "INFO" in result
    assert "ERROR" in result


def test_process_files_with_missing_file():
    """Проверяет, что обработка файлов с отсутствующим файлом вызывает ошибку."""
    with pytest.raises(FileNotFoundError):
        process_files(["nonexistent.log"], "handlers")


def test_process_files_with_invalid_report(tmp_path):
    """Проверяет, что обработка файлов с несуществующим отчетом вызывает ошибку."""
    file = tmp_path / "access.log"
    file.write_text(
        "2025-04-29 10:00:00,000 INFO django.request: GET /index 200 OK")

    with pytest.raises(ValueError):
        process_files([str(file)], "unknown_report")
