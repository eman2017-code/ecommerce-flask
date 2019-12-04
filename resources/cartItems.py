import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

# blueprint
cartItems = Blueprint('cartItems', 'cartItems')

# checkout route
# @cartItems.route('/checkout', methods=["POST"])
# # the user must be logged in
# @login_required
# def checkout():
#     # grab the cart that belongs to the user
#     # list out all the items that are in the cart
#     # list out the quantity that is in their cart
#     # add up all the prices that each item has