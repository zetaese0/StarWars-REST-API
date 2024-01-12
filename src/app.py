"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    results = list(map(lambda user: user.serialize(), all_users))
    response_body = {
        "msg": "GET /users response",
        "data": results
    }
    return jsonify(response_body), 200

# Get a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    return jsonify(user.serialize()), 200

# Get all planets
@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    results = list(map(lambda planet: planet.serialize(), all_planets))
    response_body = {
        "msg": "GET /planets response",
        "data": results
    }
    return jsonify(response_body), 200

# Get a specific planet by ID
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    return jsonify(planet.serialize()), 200

# Get all characters
@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters = Characters.query.all()
    results = list(map(lambda character: character.serialize(), all_characters))
    response_body = {
        "msg": "GET /characters response",
        "data": results
    }
    return jsonify(response_body), 200

# Get a specific character by ID
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_single_character(character_id):
    character = Characters.query.get(character_id)
    if character is None:
        raise APIException("Character not found", status_code=404)
    return jsonify(character.serialize()), 200

# Endpoint to add a new planet or planets
@app.route('/planets', methods=['POST'])
def add_planet():
    data = request.get_json()

    # Handle a single planet or a list of planets
    if isinstance(data, list):
        # If data is a list, iterate over each item and add it to the database
        for planet_data in data:
            add_single_planet(planet_data)
    elif isinstance(data, dict):
        # If data is a dictionary, add a single planet to the database
        add_single_planet(data)
    else:
        return jsonify({"error": "Invalid JSON data"}), 400

    return jsonify({"message": "Planets added successfully"}), 201

def add_single_planet(planet_data):
    name = planet_data.get('name')
    rotation_period = planet_data.get('rotation_period')
    population = planet_data.get('population')

    new_planet = Planets(name=name, rotation_period=rotation_period, population=population)
    db.session.add(new_planet)
    db.session.commit()

# Endpoint to add a new character or characters
@app.route('/characters', methods=['POST'])
def add_character():
    data = request.get_json()

    # Handle a single character or a list of characters
    if isinstance(data, list):
        # If data is a list, iterate over each item and add it to the database
        for character_data in data:
            add_single_character(character_data)
    elif isinstance(data, dict):
        # If data is a dictionary, add a single character to the database
        add_single_character(data)
    else:
        return jsonify({"error": "Invalid JSON data"}), 400

    return jsonify({"message": "Characters added successfully"}), 201

def add_single_character(character_data):
    name = character_data.get('name')
    mass = character_data.get('mass')
    height = character_data.get('height')
    hair_color = character_data.get('hair_color')

    new_character = Characters(name=name, mass=mass, height=height, hair_color=hair_color)
    db.session.add(new_character)
    db.session.commit()    



# ... other imports ...

# Endpoint to delete a planet by ID
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)

    if planet is None:
        raise APIException("Planet not found", status_code=404)

    db.session.delete(planet)
    db.session.commit()

    return jsonify({"message": "Planet deleted successfully"}), 200

# Endpoint to delete a character by ID
@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Characters.query.get(character_id)

    if character is None:
        raise APIException("Character not found", status_code=404)

    db.session.delete(character)
    db.session.commit()

    return jsonify({"message": "Character deleted successfully"}), 200

# ... other endpoints ...





# Run the app
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
