## Description:

_e-commerce site_

- This is an e-commerce site built to showcase my extended knowledge of Reactjs and SQL databases. My main focus on this project was to try and experiment with how a lot of business conduct actual business. A lot of business' purchases are done online now a days, so I thought that it would be really cool to learn how to build something that everyone uses. With my app, a user will be able to browse the website as if they were a customer, or create items to sell to others as if they were a business.

## User Stories:

- User will see the main component
- User will be able to see products page
  - within the products page, user will be able to filter what type of results they would like shown
- User will be able to use the search component to actually search for specific items
- If the user clicks on My Account and they are not logged in, they will be brought to their login/register page
  - User must sign in/register to view their cart
  - User will not be able to add something to their cart if they do not have an account
- User will be able to log out
- admin(seller/business) will be able to CRUD items in inventory
- User will be able to checkout and order their items

## Routes:

1. User/Admin

   - register route --> POST /register
   - login route --> POST /login
   - log out route --> GET /log out
   - view account route --> GET /account

2. Cart

   - update cart --> PUT /product_id/cart_id/Cart
   - add to cart -> POST /cart_id/Cart (user will be able to do this)
   - list all items in a cart --> GET /cart_id/Cart

3. Product

   - update product in cart (remove item from cart) --> PUT /product (only user can do this)
   - list all products --> GET /product (user and admin can both access this)
   - show individual product (selecting an individual product) --> GET /product_id (user and admin can both access this)
   - create product - (creating a product) --> POST /product (must be admin)
   - delete product --> Delete /product_id (must be admin)
   - update product --> PUT /product_id (must be admin)

4. Search

   - search for products --> POST /search (user and admin can both access this)

5. Checkout
   - checkout and pay for list of items --> GET /checkout

## Models:

```
class User(UserMixin, Model):
    first_name = CharField(unique = True)
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField()
    admin = BooleanField()

    class Meta:
        database = DATABASE
```

```
class Product():
    name = CharField(unique = True)
    price = IntegerField()
    description = CharField()

    class Meta:
        database = DATABASE
```

```
class Cart(Model):
    user_id = ForeignKeyField(Cart, backref='users')
    quantity = IntegerField()
    product_id = ForeignKeyField(Cart, backref='products')
    paid = BooleanField()

    class Meta:
        database = DATABASE
```

```
class CartItem():
    product_id = ForeignKeyField(CartItem, backref='products')
    cart_id = ForeignKeyField(CartItem, backref='carts')

    class Meta:
        database = DATABASE
```

```def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Product, Cart, CartItem], safe=True)
    print("Created tables if they weren't already there")
    DATABASE.close()
```

## Wireframes:

**Main Page** - https://wireframe.cc/2SSkEE

**Product Page** - https://wireframe.cc/0U21KH

**View Cart Page** - https://wireframe.cc/FJ96fp

**View Image Page** - https://wireframe.cc/3THnuo

**Login/Register Page** - https://wireframe.cc/2DCUhy

**View Account Page** - https://wireframe.cc/8wXPEW

**Search Component** - https://wireframe.cc/j4zTWv

**Check out Component** -https://wireframe.cc/DIMp3a
