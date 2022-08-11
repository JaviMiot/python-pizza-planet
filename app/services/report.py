from app.common.http_methods import GET
from flask import Blueprint

from ..controllers import ReportController
from .base_service import base_service

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
@base_service()
def get_report():
    return ReportController.generate_report()
