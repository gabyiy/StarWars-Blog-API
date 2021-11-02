"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "Secret StarWars"
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/login', methods=['GET'])
@jwt_required()
def sign_in():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email, password=password).first()
    if User is None:
        return jsonify({"msg": "Email or password is wrong"}), 401
    
    token = create_access_token(identity=user.id)
    return jsonify({"token": token}), 200

@app.route('/user', methods=['GET'])
@jwt_required()
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
@jwt_required()
def get_all_people():
    all_people = People.get_all_people()

    return jsonify(all_people), 200

@app.route('/people/<int:id>', methods = ['GET'])
@jwt_required()
def get_people(id):
    people= People.get_people(id)

    return jsonify(people),200

@app.route('/people', methods=['POST'])
@jwt_required()
def create_people():
    body = request.get_json()
    if body is None:
        return {"error": "The body is null or undefined"}, 400
    
    people = People.create_people(body['name'], body['birth_year'], body['gender'], body['height'], body['mass'], body['hair_color'], body['skin_color'], body['eye_color'] )
    
    return {"message": "people created"}, 200

@app.route('/planet', methods=['GET'])
@jwt_required()
def get_all_planets():
    planets = Planet.get_all_planets()

    return jsonify(planets), 200

@app.route('/planet/<int:id>', methods=['GET'])
@jwt_required()
def get_planet(id):
    planet = Planet.get_planet(id)

    return jsonify(planet), 200

@app.route('/planet', methods=['POST'])
@jwt_required()
def create_planet():
    body = request.get_json()
    if body is None:
        return {"error": "The body is null or undefined"}, 400
    
    planet = Planet.create_planet(body['name'], body['rotation_period'], body['orbital_period'], body['diameter'], body['climate'], body['terrain'], body['surface_water'], body['population']  )
   
    return {"message": "planet created"}, 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
@jwt_required()
def create_favorite_people():
    body = request.get_json()
    if body is None:
        return {"error": "Body is empty or null"}, 400
    
    new_people = User.get_user(body['new_people'])
    people_id = new_people.id

    people = people.get_people(new_people.id)
    people_id = people.id

    Favorite.create_favorite(user_id, people_id)

    return {"message": "Favorite people created OK"}, 200
    
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
@jwt_required()
def create_favorite_planet():
    body = request.get_json()
    if body is None:
        return {"error": "Body is empty or null"}, 400

    new_planet = User.get_user(body['new_planet'])
    planet_id = new_planet.id

    planet = Planet.get_planet(new_planet.id)
    planet_id = planet.id

    Favorite.create_favorite(user_id, planet_id)

    return {"message": "Favorite planet created OK"}, 200

@app.route('/favorite', methods=['GET'])
@jwt_required()
def get_all_favorites():
    favorites = Favorite.get_all_favorites()
    return jsonify(favorites), 200

@app.route('/favorite/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite_planet(favorite_id,planet_id):
    favorite = Favorite.delete_favorite_planet(favorite_id,planet_id)
    return jsonify(favorites),200

@app.route('/favorite/<int:people_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite_people(favorite_id,people_id):
    favorite = Favorite.delete_favorite_people(favorite_id,people_id)
    return jsonify(favorites),200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
