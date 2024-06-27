from datetime import date
from flask import Blueprint
from models.pokemon import Pokemon
from models.trainer import Trainer
from init import db, bcrypt

# Defines a Blueprint for database commands
db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def db_create():

    # Drop all existing tables (if any)
    db.drop_all()
    # Create all tables defined in the models
    db.create_all()

    # Inserting Data in DB

    trainers = [
        Trainer(
            name="Mohammed Hani",
            username="mo123",
            email="mo@email.com",
            password=bcrypt.generate_password_hash("potatoismyfav123").decode("utf-8"),
            admin=True,
        ),
        Trainer(
            name="John",
            username="John045",
            email="johnno@email.com",
            password=bcrypt.generate_password_hash("johnisnotmyname321").decode(
                "utf-8"
            ),
        ),
        Trainer(
            name="Lara",
            username="Lara007",
            email="lara123@email.com",
            password=bcrypt.generate_password_hash("tombraider2345").decode("utf-8"),
        ),
    ]
    db.session.add_all(trainers)
    db.session.commit()

    pokemons = [
        Pokemon(
            name="Squirtle",
            type="Water",
            ability="Torrent",
            date_caught=date.today(),
            trainer=trainers[0],
        ),
        Pokemon(
            name="Charmander",
            type="Fire",
            ability="Blaze",
            date_caught=date(2024, 1, 14),
            trainer=trainers[1],
        ),
        Pokemon(
            name="Pikachu",
            type="Electric",
            ability="Static",
            date_caught=date(2023, 12, 25),
            trainer=trainers[1],
        ),
        Pokemon(
            name="Mewtwo",
            type="Psychic",
            ability="telekinesis",
            date_caught=date(2023, 12, 25),
            trainer=trainers[2],
        ),
    ]
    # Similar to the Git commit command, we are adding them to the database and comitting
    db.session.add_all(pokemons)
    db.session.commit()

    # printing a message to ensure that data has been inserted successfully
    print("Pokemons and trainers have been added to the database!")
