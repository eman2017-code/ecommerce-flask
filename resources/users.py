import models

from flask import request, jsonify, Blueprint

from peewee import DoesNotExist

from flask_bcrypt import generate_password_hash, check_password_hash

from flask_login import login_user, current_user, logout_user, login_required

from playhouse.shortcuts import model_to_dict

# blueprint
users = Blueprint('users', 'users')

# register route
@users.route('/register', methods=["POST"])
def register():
    # grab the user
    payload = request.get_json()

    # make the email lowercase
    payload['email'].lower()

    try:
        # query for users email
        models.User.get(models.User.email == payload['email'])

        # return error if they come up
        return jsonify(data={}, status={"code": 401, "messsage": "A user with that email already exists"}), 401
    
    # if they didnt show up in the database via email they entered
    except models.DoesNotExist:

        # generate the password
        payload['password'] = generate_password_hash(payload['password'])
        print('payload')
        print(payload)

        # check if payload admin: "false" --> set to boolean false
        if payload['admin'] == 'False':
            payload['admin'] = False
        else:
            # otherwise it is true
            payload['admin'] = True
            
        # create the user
        user = models.User.create(**payload)

        # log them in
        login_user(user)

        # convert into dictionary
        user_dict = model_to_dict(user)

        print('user_dict')
        print(user_dict)

        # delete password
        del user_dict['password']

        # return succes
        return jsonify(data=user_dict, status={"code": 201, "message": "succesfully registered {}".format(user_dict['first_name'])}), 201

# login route
@users.route('/login', methods=["POST"])
def login():
    payload = request.get_json()

    try:
        # look up the user by their email
        user = models.User.get(models.User.email == payload['email'])
        
        # convert into dictionary
        user_dict = model_to_dict(user)

        # check the entered password
        if(check_password_hash(user_dict['password'], payload['password'])):

            # actually login the user
            login_user(user)

            # delete the password
            del user_dict['password']

            # return success
            print('user_dict')
            # print(user_dict['admin'])
            print(user_dict)
            return jsonify(data=user_dict, status={"code": 200, "message": "successfully logged in {}".format(user_dict['first_name'])}), 200
        
        # otherwise return error
        else:
            return jsonify(data={}, status={"code": 401, "message": "Email or password incorrect"}), 401
        
    # if they dont exist
    except models.DoesNotExist:
        print('they dont exist in the database')
        return jsonify(data={}, status={"code": 401, "message": "Email or password incorrect"}), 401


