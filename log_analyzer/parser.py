"""Парсер для логов Django."""
import re
from typing import Iterator, Optional

from .models import LogEntry


LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+'
    r'(?P<level>\w+)\s+'
    r'(?P<logger>\w+(\.\w+)*):\s+'
    r'(?P<message>.*)$'
)

REQUEST_PATTERN = re.compile(
    r'^(?P<method>\w+)\s+(?P<handler>/[^\s]+)\s+'
    r'(?P<status>\d+)\s+.+$'
)


def parse_log_line(line: str) -> Optional[LogEntry]:
    """Парсит строку лога и возвращает LogEntry или None, если строка невалидна."""
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None

    timestamp = match.group('timestamp')
    level = match.group('level')
    logger = match.group('logger')
    message = match.group('message')

    handler = None
    if logger == 'django.request':
        request_match = REQUEST_PATTERN.match(message)
        if request_match:
            handler = request_match.group('handler')

    return LogEntry(timestamp=timestamp, level=level, message=message, handler=handler)


def parse_log_file(file_path: str) -> Iterator[LogEntry]:
    """Генератор, который читает файл лога и возвращает LogEntry."""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            entry = parse_log_line(line)
            if entry:
                yield entry
