from sqlalchemy.exc import SQLAlchemyError

from ..repositories.managers import OrderDetailManager
from .base import BaseController


class OrderDetailController(BaseController):
    manager = OrderDetailManager

    @classmethod
    def get_top_ingredient(cls):
        try:
            return cls.manager.get_top_ingredient(), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
