from datetime import date
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
# from auth import authroize_owner
from init import db
from models.pokemon import Pokemon, PokemonSchema, pokemon_types

# Prefixing the URL for the 'pokemons' blueprint with '/pokemons' to route related endpoints
pokemons_bp = Blueprint("pokemons", __name__, url_prefix="/pokemons")


# This route handler function gets all Pokemon objects from the database
# and returns them in JSON format (R)
@pokemons_bp.route("/")
def all_pokemons():
    # Creates a SQLAlchemy select statement to retrieve all Pokemon objects
    stmt = db.select(Pokemon)
    # Executes the statement and fetches all results as a list
    pokemons = db.session.scalars(stmt).all()
    # Creates a PokemonSchema object to serialise the list of Pokemons into JSON format
    # (many=True indicates multiple Pokemon objects)
    return PokemonSchema(many=True).dump(pokemons)


# This route handler function gets a single Pokemon object based on the provided ID
# from the database and returns it in JSON format (R)
@pokemons_bp.route("/<int:id>")
def get_one_pokemon(id):
    # Uses the db.get_or_404 function to retrieve a Pokemon object with the specified ID.
    # If the object is not found, it raises a 404 Not Found exception.
    pokemon = db.get_or_404(Pokemon, id)
    # Creates a PokemonSchema object to serialise the Pokemon object into JSON format
    return PokemonSchema().dump(pokemon)

# This route handler function adds a pokemon object to the database
# and returns it in JSON format (C)
@pokemons_bp.route("/create", methods=['POST'])
def adding_pokemon():
    # Load the Pokemon data from the request body using PokemonSchema
    pokemon_info = PokemonSchema(only=["name", "type", "ability"], unknown="exclude").load(
        request.json
    )
    # Capitalise the first letter of the type
    pokemon_type = pokemon_info["type"].capitalize()
    # checks if the pokemon type matches with the existing types in the models
    if pokemon_type not in pokemon_types.enums:
        # if it does not match it sends out an error
        abort(400, description=f"This is a Invalid Pokemon type: {pokemon_info['type']}")

    # Create a new Pokemon object with the provided information
    pokemon = Pokemon(
            name=pokemon_info["name"],
            type=pokemon_info["type"].capitalize(),
            ability=pokemon_info["ability"],
            date_caught=date.today(),
    )
    # Add the new Pokemon to the database session
    db.session.add(pokemon)
    # Commit the changes to the database
    db.session.commit()
    # Return the newly created Pokemon data as JSON with a 201 sucessful Created status code
    return PokemonSchema().dump(pokemon), 201