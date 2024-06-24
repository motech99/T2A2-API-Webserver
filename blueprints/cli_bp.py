from datetime import date
from flask import Blueprint
from models.pokemon import Pokemon
from init import db

# Defines a Blueprint for database commands
db_commands = Blueprint('db', __name__)


@db_commands.cli.command('create')
def db_create():

    # Drop all existing tables (if any)
    db.drop_all()
    # Create all tables defined in the models
    db.create_all()

    # Inserting Data in our DB
    pokemons = [
        Pokemon(
                name='Squirtle',
                type='Water',
                ability='Torrent',
                date_caught=date.today(),
        ),
        Pokemon(
                name='Charmander',
                type='Fire',
                ability='Blaze',
                date_caught=date(2024, 1, 14),
        ),
        Pokemon(
                name='Pikachu',
                type='Electric',
                ability='Static',
                date_caught=date(2023, 12, 25),
        ),
    ]
    db.session.add_all(pokemons)
    db.session.commit()

print("Pokemons have been added to the database!")