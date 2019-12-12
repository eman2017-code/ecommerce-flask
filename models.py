import os
from peewee import *

from flask_login import UserMixin
from playhouse.db_url import connect

# DATABASE = SqliteDatabase('users.sqlite')

if 'ON_HEROKU' in os.environ: # later we will manually add this env var 
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this 
                                                     # env var for you 
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
  DATABASE = SqliteDatabase('users.sqlite')

  # OPTIONALLY: instead of the above line, here's how you could have your 
  # local app use PSQL instead of SQLite:

  # DATABASE = PostgresqlDatabase('dog_demo', user='reuben')  

  # the first argument is the database name -- YOU MUST MANUALLY CREATE 
  # IT IN YOUR psql TERMINAL
  # the second argument is your Unix/Linux username on your computer


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
    picture = CharField()
    name = CharField()
    price = IntegerField(default=0)
    description = CharField()
    category = CharField()

    class Meta:
        database = DATABASE

class Cart(Model):
    user_id = ForeignKeyField(User, backref='users')
    quantity = IntegerField(null = True)
    product_id = ForeignKeyField(Product, backref='products')
    paid = BooleanField(null = True)

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