import pytest
from app.controllers import ReportController


def test_generate_report_with_orders(app, create_orders):
    report, error = ReportController.generate_report()
    pytest.assume(error is None)
    pytest.assume(report['customers'] != None)
    pytest.assume(report['ingredient'] != None)
    pytest.assume(report['month'] != None)


def test_generate_report_without_orders(app):
    report, error = ReportController.generate_report()
    pytest.assume(error)
