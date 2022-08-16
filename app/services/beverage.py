from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import BeverageController
from .base_service import base_service

beverage = Blueprint('beverage', __name__)


@beverage.route('/', methods=POST)
@base_service(status_code=201)
def create_beverage():
    return BeverageController.create(request.json)


@beverage.route('/', methods=PUT)
@base_service()
def update_beverage():
    return BeverageController.update(request.json)


@beverage.route('/id/<_id>', methods=GET)
@base_service()
def get_beverage_by_id(_id: int):
    return BeverageController.get_by_id(_id)


@beverage.route('/', methods=GET)
@base_service()
def get_beverages():
    return BeverageController.get_all()
