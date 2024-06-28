from datetime import date
from flask import Blueprint, request, abort, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import admin_only, authorize_owner_pokemon
from init import db
from models.pokemon import Pokemon, PokemonSchema, pokemon_types

# Prefixing the URL for the 'pokemons' blueprint with '/pokemons' to route related endpoints
pokemons_bp = Blueprint("pokemons", __name__, url_prefix="/pokemons")


# This route handler function gets all Pokemon objects from the database
# and returns them in JSON format (R)
@pokemons_bp.route("/")
@admin_only
def all_pokemons():
    # Creates a SQLAlchemy select statement to retrieve all Pokemon objects
    stmt = db.select(Pokemon)
    # Executes the statement and fetches all results as a list
    pokemons = db.session.scalars(stmt).all()
    # Creates a PokemonSchema object to serialise the list of Pokemons into JSON format
    # (many=True indicates multiple Pokemon objects)
    return PokemonSchema(many=True).dump(pokemons)

@pokemons_bp.route("/owned")
@jwt_required()
def get_owned_pokemons():
    trainer_id = get_jwt_identity()
    # Create a SQLAlchemy select statement to retrieve all Pokémon objects owned by the trainer
    stmt = db.select(Pokemon).where(Pokemon.trainer_id == trainer_id)
    # Execute the statement and fetch all results as a list
    owned_pokemons = db.session.scalars(stmt).all()
    # Check if the authenticated user owns any Pokemon
    if not owned_pokemons:
        abort(make_response(jsonify(error="No Pokemon found for this trainer."), 404))
    # Serialise the list of owned Pokémon into JSON format
    return PokemonSchema(many=True).dump(owned_pokemons)


# This route handler function gets a single Pokemon object based on the provided ID
# from the database and returns it in JSON format (R)
@pokemons_bp.route("/<int:id>")
@jwt_required()
def get_one_pokemon(id):
    # Uses the db.get_or_404 function to retrieve a Pokemon object with the specified ID.
    # If the object is not found, it raises a 404 Not Found exception.
    pokemon = db.get_or_404(Pokemon, id)
    authorize_owner_pokemon(pokemon)
    # Creates a PokemonSchema object to serialise the Pokemon object into JSON format
    return PokemonSchema().dump(pokemon)


# This route handler function adds a pokemon object to the database
# and returns it in JSON format (C)
@pokemons_bp.route("/create", methods=["POST"])
@jwt_required()
def adding_pokemon():
    # Load the Pokemon data from the request body using PokemonSchema
    pokemon_info = PokemonSchema(
        only=["name", "type", "ability"], unknown="exclude"
    ).load(request.json)
    # Capitalise the first letter of the type to avoid errors
    pokemon_type = pokemon_info["type"].capitalize()
    # checks if the pokemon type matches with the existing types in the models
    if pokemon_type not in pokemon_types.enums:
        # if it does not match it sends out an error
        abort(
            400, description=f"This is a Invalid Pokemon type: {pokemon_info['type']}"
        )

    # Create a new Pokemon object with the provided information
    pokemon = Pokemon(
        name=pokemon_info["name"],
        type=pokemon_info["type"].capitalize(),
        ability=pokemon_info["ability"],
        date_caught=date.today(),
        trainer_id=get_jwt_identity()
    )
    # Add the new Pokemon to the database session
    db.session.add(pokemon)
    # Commit the changes to the database
    db.session.commit()
    # Return the newly created Pokemon data as JSON with a 201 sucessful Created status code
    return PokemonSchema().dump(pokemon), 201


# This route handler function that updates a existing pokemon object in the database
# and returns it in JSON format upon successful update (U)
@pokemons_bp.route("/update/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_pokemon(id):
    # Fetch the Pokemon object with the given ID from the database
    # Raise a 404 error if the Pokemon is not found
    pokemon = db.get_or_404(Pokemon, id)
    authorize_owner_pokemon(pokemon)
    # Use PokemonSchema to validate and deserialise the incoming JSON data
    # Only allow updates to "name", "type", and "ability" fields ignoring any unknown fields
    pokemon_info = PokemonSchema(
        only=["name", "type", "ability"], unknown="exclude"
    ).load(request.json)
    # Capitalise the first letter of the type to avoid errors
    pokemon_type = pokemon_info["type"].capitalize()
    # checks if the pokemon type matches with the existing types in the models
    if pokemon_type not in pokemon_types.enums:
    # if it does not match it sends out an error
        abort(
            400, description=f"This is a Invalid Pokemon type: {pokemon_info['type']}"
        )
    # Update the Pokemon object's attributes with the provided data
    pokemon.name = pokemon_info.get('name', pokemon.name)
    pokemon.type = pokemon_info.get('type', pokemon.type).capitalize()
    pokemon.ability = pokemon_info.get('ability', pokemon.ability)
    # Commit the changes to the database
    db.session.commit()
    # Return a 200 OK response with the only requested JSON representation
    return PokemonSchema(only=['name', 'type', 'ability']).dump(pokemon), 200


# Delete an existing Pokemon (D)
@pokemons_bp.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_pokemon(id):
    # Fetch a pokemon record by ID, raising 404 if not found
    pokemon = db.get_or_404(Pokemon, id)
    authorize_owner_pokemon(pokemon)
    # Delete the pokemon object
    db.session.delete(pokemon)
    db.session.commit()
    return jsonify({"message": "The pokemon has successfully been deleted!"})
