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
		product = models.Product.create(
			name=payload["name"], 
			price=payload["price"], 
			description=payload["description"], 
			picture=payload["picture"], 
			category=payload["category"], 
			owner=current_user.id)
		# change the model to dictionary
		product_dict = model_to_dict(product)
		# dont show the password of the user
		product_dict['owner'].pop('password')	
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

# # product show route
# @products.route('/<product_id>', methods=["GET"])
# # the user does not have to be logged in
# def show_one_product(product_id):
# 	# get the product
# 	product = models.Product.get_by_id(product_id)
# 	# make into a dictionary
# 	product_dict = model_to_dict(product)
# 	# dont show the owner of the product's password
# 	product_dict['owner'].pop('password')
# 	# return success
# 	return jsonify(data=product_dict, status={"code": 200, "message": "Successfully showed product"}), 200


# search for products
@products.route('/find', methods=["POST"])
# the user does not have to be logged in to search for products
def find_products():
	# get the data from the client
	data = request.get_json()

	# query all the products by the search string
	results = Product.select().where(Product.name.contains(data['value']) | Product.price.contains(data['value']) | Product.description.contains(data['value']))

	# iterate over all the searches -- convert to dictionaries
	results_list = []
	for result in results:
		result_dict = model_to_dict(result, backref=True, recurse=True)
		del result_dict['password']
		results_list.append(result_dict)

	# return success
	return jsonify(data=results_list, status={"code": 200, "message": "Successfully got the search results"})

# show items admin has created
@products.route('/<user_id>', methods=["GET"])
# the user must be logged in to see the products that they created
@login_required
def show_user_created_products(user_id):
		this_admins_products_instances = models.Product.select().where(models.Product.owner.id == current_user.id)
		# loop through all the products that a user has
		this_admins_products_dicts = [model_to_dict(product) for product in this_admins_products_instances ]
		return jsonify(data=this_admins_products_dicts, status={"code": 200, "message": "Success showing courses"})












