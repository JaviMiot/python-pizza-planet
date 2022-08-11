from sqlalchemy.exc import SQLAlchemyError

from ..repositories.reports import BasicReportFactory


class ReportController():

    @classmethod
    def generate_report(cls):
        try:
            report = BasicReportFactory()
            return report.get_report().generate_report(), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
