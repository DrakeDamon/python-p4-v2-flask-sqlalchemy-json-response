from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return make_response(
        '<h1>Welcome to the pet directory!</h1>',
        200
    )

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    print(f"Accessing pet {id}")
    print(f"Found pet: {pet}")

    if pet:
        body = {
            'id': pet.id,
            'name': pet.name,
            'species': pet.species
        }
        return jsonify(body), 200
    else:
        return jsonify({'message': f'Pet {id} not found.'}), 404

@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = []  # array to store a dictionary for each pet
    for pet in Pet.query.filter_by(species=species).all():
        pet_dict = {
            'id': pet.id,
            'name': pet.name,
        }
        pets.append(pet_dict)
    body = {
        'count': len(pets),
        'pets': pets
    }
    return make_response(jsonify(body), 200)

if __name__ == '__main__':
    app.run(port=5556, debug=True)