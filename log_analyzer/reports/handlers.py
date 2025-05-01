"""
Модуль для генерации отчётов по обработчикам логов.

Этот модуль предоставляет функции для генерации, объединения и форматирования
отчётов по обработчикам логов. Отчёты содержат информацию о количестве
лог-записей для каждого обработчика и уровня логирования.
"""

from collections import defaultdict
from typing import Dict, List

from log_analyzer.models import LogEntry, ReportData
from log_analyzer.reports.base import Report


class HandlersReport(Report):
    """Класс отчёта по обработчикам логов."""

    def __init__(self):
        self.data: ReportData = ReportData(handlers={}, total=0)

    def generate(self, entries: List[LogEntry]) -> str:
        self._collect(entries)
        return self._format()

    def _collect(self, entries: List[LogEntry]):
        handler_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        total = 0

        for entry in entries:
            if entry.handler and entry.level:
                handler_stats[entry.handler][entry.level] += 1
                total += 1

        self.data = ReportData(handlers=dict(handler_stats), total=total)

    def _format(self) -> str:
        if not self.data.handlers:
            return "No data to display\n"

        all_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        handler_keys = list(self.data.handlers.keys()) + ['HANDLER']
        handler_width = max(len(handler) for handler in handler_keys)

        level_widths = [
            max(len(level), *(len(str(self.data.handlers[h].get(level, 0))) for h in self.data.handlers))
            for level in all_levels
        ]

        def format_row(items, widths):
            return "  ".join(item.ljust(width) for item, width in zip(items, widths))

        widths = [handler_width] + level_widths
        header = format_row(["HANDLER"] + all_levels, widths)

        rows = []
        for handler in sorted(self.data.handlers.keys()):
            counts = [str(self.data.handlers[handler].get(level, 0)) for level in all_levels]
            rows.append(format_row([handler] + counts, widths))

        total_counts = [
            str(sum(self.data.handlers[handler].get(level, 0) for handler in self.data.handlers))
            for level in all_levels
        ]
        total_line = format_row([""] + total_counts, widths)

        return "\n".join([
            f"Total requests: {self.data.total}\n",
            header,
            *rows,
            total_line
        ])
