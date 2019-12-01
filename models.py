import datetime

from peewee import *

from flask_login import UserMixin

DATABASE = SqliteDatabase('users.sqlite')


class User(UserMixin, Model):
    first_name = CharField(unique = True)
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField()
    admin = BooleanField()

    class Meta:
        database = DATABASE

class Product():
    name = CharField(unique = True)
    price = IntegerField()
    description = CharField()

    class Meta:
        database = DATABASE

class Cart(Model):
    user_id = ForeignKeyField(Cart, backref='users')
    quantity = IntegerField()
    product_id = ForeignKeyField(Cart, backref='products')
    paid = BooleanField()

    class Meta:
        database = DATABASE

class CartItem():
    product_id = ForeignKeyField(CartItem, backref='products')
    cart_id = ForeignKeyField(CartItem, backref='carts')

    class Meta:
        database = DATABASE


def initialize():
    # connect to the database
    DATABASE.connect()
    DATABASE.create_tables([User, Product, Cart, CartItem], safe=True)
    print("Created tables if they weren't already there")
    DATABASE.close()