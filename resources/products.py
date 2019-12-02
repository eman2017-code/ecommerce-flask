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

# delete product route
@products.route('/<id>', methods=["Delete"])

# the admin must be logged in
@login_required

def delete_product(id):

	# get the product by its id
	product_to_delete = models.Product.get_by_id(id)

	# check to see that the product that is being deleted belongs to the admin
	if product_to_delete.owner.id != current_user.id:
		return jsonify(data={}, status={"code": 403, "message": "you can only delete your own products"})

	# if it matches, delete the product
	else:
		# variable to show the name of the product
		product_name = product_to_delete.name

		product_to_delete.delete_instance()
		return jsonify(data="product successfully deleted", status={"code": 200, "message": "{} deleted successfully".format(product_name)})
	
		
# update product route
@products.route('/<id>', methods=["PUT"])

# the admin must be logged in
@login_required

def update_product(id):
	payload = request.get_json()

	# get the product by its id
	product = models.Product.get_by_id(id)

	# only if the product belongs to the admin
	if (product.owner.id == current_user.id):
		product.name = payload['name'] if 'name' in payload else None
		product.price = payload['price'] if 'price' in payload else None
		product.description = payload['description'] if 'description' in payload else None

		# save the changes made to the product
		product.save()

		product_dict = model_to_dict(product)
		# dont show the password of the user
		product_dict['owner'].pop('password')

		# return success
		return jsonify(data=product_dict, status={"code": 200, "message": "Product successfully updated"}), 200

	# if the product does not belong to the user
	else:
		# return error
		return jsonify(data={}, status={"code": 403, "message": "You can only edit items that you posted"}), 403







