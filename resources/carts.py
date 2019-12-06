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

# list items in specific cart
@carts.route('/<user_id>', methods=["GET"])
# the user must be logged in to to see all of their itmes that they have in their cart
@login_required
def list_items_in_cart(user_id):
    # get all the cart intances that have the current users id
    this_users_cart_instances = models.Cart.select().where(models.Cart.user_id == current_user.id)
    # loop to show all the cart items
    this_users_carts_dicts = [model_to_dict(cart) for cart in this_users_cart_instances]

    # return success
    return jsonify(data=this_users_carts_dicts, status={"code": 200, "message": "Here are the carts"})

# # show items admin has created
# @carts.route('/my_items/<user_id>', methods=["GET"])
# # the user must be logged in to see the products that they created
# @login_required
# def show_user_created_products(user_id):
# 	this_admins_products_instances = models.Product.select().where(models.Product.owner.id == current_user.id)
# 	# loop through all the products that a user has
# 	this_admins_products_dicts = [model_to_dict(product) for product in this_admins_products_instances ]
# 	return jsonify(data=this_admins_products_dicts, status={"code": 200, "message": "Success showing courses"})
    

    
    