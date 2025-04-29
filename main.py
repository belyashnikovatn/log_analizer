"""
CLI-приложение для анализа логов Django-приложения.

Обрабатывает файлы логов и генерирует отчёты.
"""
import argparse
from pathlib import Path
from typing import List, Optional

from log_analyzer.parser import parse_log_file
from log_analyzer.reports.handlers import (
    generate_handlers_report,
    merge_reports,
    format_handlers_report
)


REPORTS = {
    'handlers': {
        'generator': generate_handlers_report,
        'merger': merge_reports,
        'formatter': format_handlers_report
    }
}


def process_files(file_paths: List[str], report_name: str) -> Optional[str]:
    """Обрабатывает файлы и возвращает сформированный отчёт."""
    if report_name not in REPORTS:
        raise ValueError(f"Unknown report: {report_name}. Available reports: {list(REPORTS.keys())}")

    # Проверяем существование файлов
    for file_path in file_paths:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    report_generator = REPORTS[report_name]['generator']
    report_merger = REPORTS[report_name]['merger']
    report_formatter = REPORTS[report_name]['formatter']

    reports = []
    for file_path in file_paths:
        log_entries = list(parse_log_file(file_path))
        report = report_generator(log_entries)
        reports.append(report)

    merged_report = report_merger(reports)
    return report_formatter(merged_report)


def main():
    """Точка входа CLI-приложения."""
    parser = argparse.ArgumentParser(description='Analyze Django application logs.')
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
        choices=REPORTS.keys(),
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
