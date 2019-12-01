from flask import Flask, jsonify, g
# from flask_cors import CORS

# from flask_login import LoginManager

DEBUG = True 
PORT = 8000

# from resources.users import users
# from resources.products import products
# from resources.carts import carts
# from resources.cartItems import cartItems

# import models

app = Flask(__name__)  

# app.secret_key = "this is a secret key that only the jedi can see"

# login_manager = LoginManager()

# login_manager.init_app(app)

# CORS(users, origins=['http://localhost:3000'], supports_credentials=True) 
# CORS(products, origins=['http://localhost:3000'], supports_credentials=True)
# CORS(carts, origins=['http://localhost:3000'], supports_credentials=True)
# CORS(cart_items, origins=['http://localhost:3000'], supports_credentials=True)

# app.register_blueprint(users, url_prefix='/api/v1/users')
# app.register_blueprint(products, url_prefix='/api/v1/products')
# app.register_blueprint(carts, url_prefix='/api/v1/carts')
# app.register_blueprint(cart_items, url_prefix='/api/v1/cart_items')

@app.before_request 
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response 

# to test that this is actually working
@app.route('/')
def index():
    return 'Hello, world!'

if __name__ == '__main__': 
  # models.initialize()
  app.run(debug=DEBUG, port=PORT)