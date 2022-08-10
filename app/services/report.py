from app.common.http_methods import GET
from flask import Blueprint, jsonify, request

from ..controllers import OrderDetailController, OrderController

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    ingredient, error = OrderDetailController.get_top_ingredient()
    month_revenue, error = OrderController.get_month_revenue()
    best_customers, error = OrderController.get_best_customers()

    return {'ingredient': ingredient, 'month': month_revenue, 'customers': best_customers}
