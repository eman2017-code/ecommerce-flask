import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

# blueprint
cartItems = Blueprint('cartItems', 'cartItems')

# checkout route
@cartItems.route('/<cart_id>', methods=["GET"])
# the user must be logged in
@login_required
def get_total_price_of_items(cart_id):
    try:
        # get instance of the specific cart that the user is
        user_cart_instances = (models.Cart.select().where(models.Cart.user_id == current_user.id))
        # convert them into dictionaries
        user_cart_instances_dicts = [model_to_dict(carts) for carts in user_cart_instances]
        # get the prices
        price_list = []
        for cart in user_cart_instances_dicts:
            price_list.append(cart['product_id']['price'])

        # user_cart_instances_dicts_prices = user_cart_instances_dicts['price']
        # return success
        return jsonify(data=price_list, status={"code": 200, "message": "Success getting all the carts"}), 200
    except models.DoesNotExist:
        # return the error
        return jsonify(data={}, status={"code": 401, "messsage": "Error getting this resource"}), 401


