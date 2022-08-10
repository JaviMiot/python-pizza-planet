from flask_seeder import Seeder, Faker, generator
from datetime import datetime, timezone

from app.seeds.generators import SequenceArray, DateGenerator, NameGenerator
from app.repositories.models import Beverage, Size, Ingredient, Order, OrderDetail

# faker data
pizza_sizes = [
    {'name': 'personal', 'price': 1},
    {'name': 'small', 'price': 5},
    {'name': 'medium', 'price': 10},
    {'name': 'large', 'price': 15},
    {'name': 'extra large', 'price': 20}]

ingredient_names = ['salami', 'pepper',
                    'cheese', 'tomato',
                    'mushrooms', 'onion',
                    'garlic', 'bacon',
                    'hot papper', 'egg']
beverage_names = ['Fanta', 'Coca-Cola', 'Sprite', 'Inca Kola', 'Bimbo']

total_orders = 200


class DdSeeder(Seeder):

    def generate_items(self, model, data: list):
        faker = Faker(
            cls=model,
            init={
                '_id': generator.Sequence(end=total_orders),
                'name': SequenceArray(data),
                'price': generator.Integer(1, 15)
            }
        )

        return faker

    def generate_size(self):
        names = [size['name']for size in pizza_sizes]
        prices = [size['price']for size in pizza_sizes]

        size_faker = Faker(
            cls=Size,
            init={
                '_id': generator.Sequence(end=total_orders),
                'name': SequenceArray(names),
                'price': SequenceArray(prices)
            }
        )

        return size_faker

    def generate_order(self):
        order_faker = Faker(
            cls=Order,
            init={
                '_id': generator.Sequence(end=total_orders),
                'client_name': NameGenerator(),
                'client_dni': generator.String('[1-9]{4}-[1-9]{4}'),
                'client_address': generator.String('\c{8}-\c{8}'),
                'client_phone': generator.String('[5-9]{4}-[0-9]{9}'),
                'date': DateGenerator(start_date=datetime(2022, 1, 1, tzinfo=timezone.utc)),
                'total_price': 0,
                'size_id': generator.Integer(start=1, end=len(pizza_sizes))}
        )

        order_detail_faker = Faker(
            cls=OrderDetail,
            init={
                '_id': generator.Sequence(end=total_orders),
                'ingredient_price': 0,
                'order_id': generator.Integer(start=1, end=total_orders),
                'ingredient_id': generator.Integer(start=1, end=len(ingredient_names)),
            }
        )

        orders_created = [order for order in order_faker.create(total_orders)]
        orders_details_created = [
            order_detail for order_detail in order_detail_faker.create(total_orders)]

        return orders_created, orders_details_created

    def save_data(self, data):
        for register in data:
            self.db.session.add(register)

    def run(self):
        """Method to populate the db with faker data
        """
        ingredients = [ingredient for ingredient in self.generate_items(
            Ingredient, ingredient_names).create(len(ingredient_names))]

        beverage = [beverage for beverage in self.generate_items(
            Beverage, beverage_names).create(len(beverage_names))]

        sizes = [size for size in self.generate_size().create(len(pizza_sizes))]

        orders_created, orders_details_created = self.generate_order()

        # Calculate price of ingredients to store in order detail table
        for order_detail in orders_details_created:
            order_detail.ingredient_price = sum(
                [ingredient.price for ingredient in ingredients
                 if ingredient._id == order_detail.ingredient_id])

         # Calculate total price to store in order table
        for order in orders_created:
            total_ingredients = sum([
                detail.ingredient_price for detail in orders_details_created
                if detail.order_id == order._id])

            size_price = sum(
                [size.price for size in sizes if size._id == order.size_id])

            order.total_price = total_ingredients + size_price

        # Save faker data in db
        self.save_data(ingredients)
        self.save_data(beverage)
        self.save_data(sizes)
        self.save_data(orders_created)
        self.save_data(orders_details_created)
