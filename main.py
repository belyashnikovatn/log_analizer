"""
CLI-приложение для анализа логов Django-приложения.

Обрабатывает файлы логов и генерирует отчёты.
"""

import argparse
from pathlib import Path
from typing import List

from log_analyzer.parser import parse_log_file
from log_analyzer.reports import get_report_generator  # фабрика
from log_analyzer.reports.base import Report


def process_files(file_paths: List[str], report_name: str) -> str:
    """Обрабатывает файлы и возвращает сформированный отчёт."""
    # Проверка существования файлов
    for file_path in file_paths:
        if not Path(file_path).is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

    report_generator: Report = get_report_generator(report_name)

    # Собираем логи со всех файлов
    all_entries = []
    for file_path in file_paths:
        all_entries.extend(parse_log_file(file_path))

    return report_generator.generate(all_entries)


def main():
    """Точка входа CLI-приложения."""
    parser = argparse.ArgumentParser(
        description='Analyze Django application logs.')
    parser.add_argument(
        'files',
        metavar='FILE',
        type=str,
        nargs='+',
        help='log files to analyze'
    )
    parser.add_argument(
        '--report',
        type=str,
        required=True,
        choices=['handlers'],
        help='report type to generate'
    )

    args = parser.parse_args()

    try:
        report = process_files(args.files, args.report)
        print(report)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == '__main__':
    main()
