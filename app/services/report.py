from app.common.http_methods import GET
from flask import Blueprint, jsonify, request

from ..controllers import ReportController

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    report, error = ReportController.generate_report()
    response = report if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code
