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

# list all products route
@products.route('/', methods=["GET"])
# the user does not have to be logged in to see all the products that are offered
def list_products():
	try:
		# select all of the data from the Product model and store it into the product_instances varaible 
		product_instances = models.Product.select()
		
		# loop through all the products currently in the database
		product_instances_dict = [model_to_dict(products) for products in product_instances]

		# return success
		return jsonify(data=product_instances_dict, status={"code": 200, "message": "Sucess"}), 200

	# if the data cannot be processed
	except:
		return jsonify(data={}, status={"code": 500, "message": "the data cannot be processed"})






