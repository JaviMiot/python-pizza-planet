from sqlalchemy.exc import SQLAlchemyError

from typing import Any, List, Optional, Sequence
from sqlalchemy.sql import text, column
from sqlalchemy import func, desc

from .models import Ingredient, Order, OrderDetail, BeverageDetail, Size, db, Beverage
from .serializers import (IngredientSerializer, OrderSerializer,
                          SizeSerializer, BeverageSerializer, ma)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class BaseReportManager:
    order_model: Optional[db.Model] = None
    order_detail_model: Optional[db.Model] = None
    session = db.session

    @staticmethod
    def orders_not_found(model):
        if not model:
            raise SQLAlchemyError("don't have orders")

    @classmethod
    def get_top_ingredient(cls):
        _object = cls.session.query(func.count(
            cls.order_detail_model.ingredient_id).label('count'),
            cls.order_detail_model.ingredient_id).group_by(cls.order_detail_model.ingredient_id).order_by(desc('count')).first()

        cls.orders_not_found(_object)

        ingredient = Ingredient.query.get(_object.ingredient_id)
        top_ingredient = {
            'name': ingredient.name,
            'count': _object.count
        }
        return top_ingredient

    @classmethod
    def get_month_revenue(cls):
        month = cls.session.query(
            func.strftime("%m", cls.order_model.date).label('month'),
            func.sum(cls.order_model.total_price).label('total')).group_by('month').order_by(desc('total')).first()

        cls.orders_not_found(month)

        return {'month_number': month[0], 'total': month[1]}

    @classmethod
    def get_best_customers(cls):
        customers = cls.session.query(
            cls.order_model.client_name, cls.order_model.client_dni,
            func.count(cls.order_model.client_dni).label('count')
        ).group_by(cls.order_model.client_dni).order_by(desc('count')).limit(3).all()

        cls.orders_not_found(customers)

        return [{'posicion': pos + 1, 'name': customer.client_name, 'dni': customer.client_dni}
                for pos, customer in enumerate(customers)]


class ListManager(BaseManager):
    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(ListManager):
    model = Ingredient
    serializer = IngredientSerializer


class BeverageManager(ListManager):
    model = Beverage
    serializer = BeverageSerializer


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all((OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id, ingredient_price=ingredient.price)
                             for ingredient in ingredients))
        cls.session.add_all((BeverageDetail(order_id=new_order._id, beverage_id=beverage._id, beverage_price=beverage.price)
                             for beverage in beverages))
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')


class ReportManager(BaseReportManager):
    order_model = Order
    order_detail_model = OrderDetail

    @classmethod
    def generate_report(cls):
        best_ingredient = cls.get_top_ingredient()
        best_month = cls.get_month_revenue()
        best_customers = cls.get_best_customers()

        report = {'ingredient': best_ingredient,
                  'month': best_month,
                  'customers': best_customers
                  }

        return report


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()
