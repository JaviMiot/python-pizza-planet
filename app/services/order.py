from app.common.http_methods import GET, POST
from flask import Blueprint, request

from ..controllers import OrderController
from .base_service import base_service

order = Blueprint('order', __name__)


@order.route('/', methods=POST)
@base_service()
def create_order():
    return OrderController.create(request.json)


@order.route('/id/<_id>', methods=GET)
@base_service()
def get_order_by_id(_id: int):
    return OrderController.get_by_id(_id)


@order.route('/', methods=GET)
@base_service()
def get_orders():
    return OrderController.get_all()
