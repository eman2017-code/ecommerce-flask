import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

# blueprint
cartItems = Blueprint('cartItems', 'cartItems')

# # checkout route
# @cartItems.route('/checkout', methods=["GET"])
# # the user must be logged in
# @login_required
# def checkout_cart():
#     # loop through all of the prices
    
#     # return success
#     # return jsonify(data="it works", status={"code": 200, "message": "blah blah blah"})