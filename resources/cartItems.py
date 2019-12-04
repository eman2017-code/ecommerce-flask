import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

# blueprint
cartItems = Blueprint('cartItems', 'cartItems')

# checkout route
@cartItems.route('/totalPrice', methods=["GET"])
# the user must be logged in
@login_required
def get_total_price_of_items():
    # loop through all of the prices that in the users cart and them add them up