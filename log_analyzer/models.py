"""
Модуль для представления данных и классов, используемых в анализаторе логов.

Содержит классы для представления записи лога, статистики по
обработчикам и данных отчёта.
"""
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class LogEntry:
    """Класс для представления записи лога."""

    timestamp: str
    level: str
    message: str
    handler: Optional[str] = None


@dataclass
class HandlerStats:
    """Класс для представления статистики по обработчикам."""

    handler: str
    counts: Dict[str, int]


@dataclass
class ReportData:
    """Класс для представления данных отчёта."""

    handlers: Dict[str, Dict[str, int]]
    total: int
