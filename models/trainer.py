from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Enum
from marshmallow.validate import Length, Regexp
from marshmallow import fields
from init import db, ma


# Creating an Enum for Gym types
gym_types = Enum(
    "Mystic",
    "Valor",
    "Instinct",
    name="gym_types",
)

# Defining the Trainer model
class Trainer(db.Model):
    """
    This class represents a Trainer in the database.
    """

    __tablename__ = "trainers"

    # Defining model attributes (columns)
    id: Mapped[int] = mapped_column(primary_key=True)
        # Primary key for the table

    name: Mapped[str] = mapped_column(String(200))
        # Trainer name (string, maximum length 200 characters)

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
        # Trainer username (unique, string, maximum length 100 characters, not nullable)

    email: Mapped[str] = mapped_column(String(100), unique=True)
        # Trainer email (unique, string, maximum length 100 characters)

    password: Mapped[str] = mapped_column(String(100))
        # Trainer password (hashed string, maximum length 100 characters)

    team: Mapped[str] = mapped_column(gym_types, nullable=False)
        # Trainer's Gym team (uses the 'gym_types' Enum, not nullable)

    admin: Mapped[bool] = mapped_column(Boolean(), server_default="false")
        # Flag indicating if the trainer is an admin (boolean, defaults to False)

    pokemons: Mapped[List["Pokemon"]] = relationship(back_populates="trainer")
        # Relationship with the 'Pokemon' model (one trainer can have many pokemons)

# Defining the TrainerSchema for serialisation and validation
class TrainerSchema(ma.Schema):
    """
    This class defines the Marshmallow schema for the Trainer model.
    It specifies how Trainer objects are serialised and validated.
    """

    username = fields.String(
        validate=[
            Length(max=15, error="Username cannot be longer than 15 characters!"),
            Regexp(
                "^[a-zA-Z0-9]+$",
                error="Username must contain only letters and numbers.",
            ),
        ],
        required=True,
    )
    password = fields.String(
        validate=Length(min=10, error="Password must be at least 10 characters long!"),
        load_only=True,
    )

    class Meta:
        fields = ("id", "name", "email", "username", "password", "team", "admin")