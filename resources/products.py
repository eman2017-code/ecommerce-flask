import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

# blueprint
products = Blueprint('products', 'products')


# create product route
@products.route('/', methods=["POST"])

# the user must be logged in
@login_required

def create_product():
	payload = request.get_json()

	# the user must be an admin to create a product
	if current_user.admin == True:
		product = models.Product.create(name=payload["name"], price=payload["price"], description=payload["description"], owner=current_user.id)

		# change the model to dictionary
		product_dict = model_to_dict(product)
		
		# return success
		return jsonify(data=product_dict, status={"code": 201, "message": "successfully created your product"}), 201
	else:
		# if the user is not an admin, they will be thrown an error
		return jsonify(data={}, status={"code": 403, "message": "You cannot create product! You are not an admin"})






