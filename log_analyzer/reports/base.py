from abc import ABC, abstractmethod
from typing import List
from log_analyzer.models import LogEntry


class Report(ABC):
    @abstractmethod
    def generate(self, entries: List[LogEntry]) -> str:
        """Сгенерировать отчёт по списку логов"""
        pass
