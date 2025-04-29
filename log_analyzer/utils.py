"""Модуль для вспомогательных функций, используемых в проекте."""
from typing import List


def validate_file_paths(file_paths: List[str]) -> bool:
    """Проверяет, что все файлы существуют."""
    for file_path in file_paths:
        try:
            with open(file_path, 'r'):
                pass
        except IOError:
            return False
    return True
