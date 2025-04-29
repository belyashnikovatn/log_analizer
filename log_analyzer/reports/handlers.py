"""
Модуль для генерации отчётов по обработчикам логов.

Этот модуль предоставляет функции для генерации, объединения и форматирования
отчётов по обработчикам логов. Отчёты содержат информацию о количестве
лог-записей для каждого обработчика и уровня логирования.
"""

from collections import defaultdict
from typing import Dict, List

from log_analyzer.models import LogEntry, ReportData


def generate_handlers_report(log_entries: List[LogEntry]) -> ReportData:
    """Генерирует отчет по handlers на основе списка лог-записей."""
    handler_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    total = 0

    for entry in log_entries:
        if entry.handler and entry.level:
            handler_stats[entry.handler][entry.level] += 1
            total += 1

    return ReportData(handlers=handler_stats, total=total)


def merge_reports(reports: List[ReportData]) -> ReportData:
    """Объединяет несколько отчетов в один."""
    merged_handlers: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))
    total = 0

    for report in reports:
        for handler, levels in report.handlers.items():
            for level, count in levels.items():
                merged_handlers[handler][level] += count
        total += report.total

    return ReportData(handlers=dict(merged_handlers), total=total)


def format_handlers_report(report: ReportData) -> str:
    """Форматирует отчёт с выравниванием всех колонок."""
    if not report.handlers:
        return "No data to display\n"

    # Все уровни логирования в требуемом порядке
    all_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    # Определяем максимальные ширины для каждой колонки
    handler_keys = list(report.handlers.keys()) + ['HANDLER']
    handler_width = max(len(handler) for handler in handler_keys)
    level_widths = [
        max(len(level), *(len(str(report.handlers[h].get(level, 0))) for h in report.handlers))
        for level in all_levels
    ]

    # Функция для форматирования строки
    def format_row(items, widths):
        return "  ".join(item.ljust(width) for item, width in zip(items, widths))

    # Ширины всех колонок
    widths = [handler_width] + level_widths

    # Заголовок
    header = format_row(["HANDLER"] + all_levels, widths)

    # Строки данных
    rows = []
    for handler in sorted(report.handlers.keys()):
        counts = [str(report.handlers[handler].get(level, 0)) for level in all_levels]
        rows.append(format_row([handler] + counts, widths))

    # Итоговая строка
    total_counts = [
        str(sum(report.handlers[handler].get(level, 0) for handler in report.handlers))
        for level in all_levels
    ]
    total_line = format_row([""] + total_counts, widths)

    # Собираем отчет
    output = [
        f"Total requests: {report.total}\n",
        header,
        *rows,
        total_line
    ]

    return "\n".join(output)
