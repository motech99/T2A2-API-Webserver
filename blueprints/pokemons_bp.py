from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
# from auth import authroize_owner
from init import db
from models.pokemon import Pokemon, PokemonSchema

# Prefixing the URL for the 'pokemons' blueprint with '/pokemons' to route related endpoints
pokemons_bp = Blueprint("pokemons", __name__, url_prefix="/pokemons")

# Get all Pokemons (R)
@pokemons_bp.route("/")
def all_pokemons():
    stmt = db.select(Pokemon)
    pokemons = db.session.scalars(stmt).all()
    return PokemonSchema(many=True).dump(pokemons)

# Get One Pokemon (R)
@pokemons_bp.route("/<int:id>")
def get_one_pokemon(id):
    pokemon = db.get_or_404(Pokemon, id)
    return PokemonSchema().dump(pokemon)
