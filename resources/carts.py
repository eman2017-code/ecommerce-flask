import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

# blueprint
carts = Blueprint('carts', 'carts')

# create cart route
# the cart gets created when the user adds an item
@carts.route('/<product_id>', methods=["POST"])
# the user must be logged in to add things to their cart
@login_required
# this id is the product id
def create_cart(product_id):
    # get the payload
    payload = request.get_json()
    # create the cart
    cart = models.Cart.create(quantity=payload['quantity'], paid=payload['paid'], product_id=product_id, user_id=current_user.id)
    # make this into a dictionary
    cart_dict = model_to_dict(cart)
    # return success
    return jsonify(data=cart_dict, status={"code": 201, "message": "You successfully created your cart"})

# route to list all the items that are in a cart
@carts.route('/', methods=["GET"])
# the user must be logged in
@login_required
def list_products_in_cart():
    try:
        # find the cart that belongs to the user
        this_users_cart_instances = models.Cart.select().where(models.Cart.user_id == current_user.id)

        this_users_cart_dicts = [model_to_dict(cart) for cart in this_users_cart_instances]

        return jsonify(data=this_users_cart_dicts, status={"code": 200, "message": "Success getting resources"})

    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "there was an error getting the resources"})
    

    
    