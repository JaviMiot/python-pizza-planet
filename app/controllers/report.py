from sqlalchemy.exc import SQLAlchemyError

from ..repositories.managers import ReportManager
from .base import BaseReportController


class ReportController(BaseReportController):
    manager = ReportManager

    @classmethod
    def generate_report(cls):
        try:
            return cls.manager.generate_report(), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
