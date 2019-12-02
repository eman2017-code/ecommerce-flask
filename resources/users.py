import models

from flask import request, jsonify, Blueprint

from peewee import DoesNotExist

from flask_bcrypt import generate_password_hash, check_password_hash

from flask_login import login_user, current_user, logout_user, login_required

from playhouse.shortcuts import model_to_dict

# blueprint
users = Blueprint('users', 'users')