import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

# blueprint
carts = Blueprint('carts', 'carts')

# create cart route
# the cart gets created when the user adds an item
@carts.route('/', methods=["POST"])

# the user must be logged in to add things to their cart
@login_required

def create_cart():

    # get the payload
    payload = request.get_json()

    # create the cart
    cart = models.Cart.create(quantity=payload['quantity'], product_id=payload['product_id'], paid=payload['paid'], user_id=payload['user_id'])

    print(model_to_dict(cart), "model_to_of_created_product")
    cart_dict = model_to_dict(cart)

    # return success
    return jsonify(data=cart_dict, status={"code": 201, "message": "You successfully created your cart"})