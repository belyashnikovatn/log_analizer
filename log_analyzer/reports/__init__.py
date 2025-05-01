from .handlers import HandlersReport
from .base import Report


def get_report_generator(name: str) -> Report:
    mapping = {
        "handlers": HandlersReport,
    }
    return mapping.get(name, HandlersReport)()
