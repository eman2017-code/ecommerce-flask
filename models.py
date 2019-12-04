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

class Product(Model):
    owner = ForeignKeyField(User, backref="users")
    name = CharField(unique = True)
    price = IntegerField()
    description = CharField()
    category = CharField()
    

    class Meta:
        database = DATABASE


class Cart(Model):
    user_id = ForeignKeyField(User, backref='users')
    quantity = IntegerField()
    product_id = ForeignKeyField(Product, backref='products')
    paid = BooleanField()

    class Meta:
        database = DATABASE

class CartItem(Model):
    product_id = ForeignKeyField(Product, backref='products')
    cart_id = ForeignKeyField(Cart, backref='carts')

    class Meta:
        database = DATABASE


def initialize():
    # connect to database
    DATABASE.connect()
    DATABASE.create_tables([User, Product, Cart, CartItem], safe=True)
    print("THE TABLES HAVE BEEN CREATED!")
    DATABASE.close()
