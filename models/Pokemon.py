from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, ForeignKey
from marshmallow import fields
from marshmallow.validate import Regexp
from init import db, ma

# Creating an Enum for Pokemon types
pokemon_types = Enum(
    "Normal",
    "Fire",
    "Water",
    "Electric",
    "Grass",
    "Ice",
    "Fighting",
    "Poison",
    "Ground",
    "Flying",
    "Psychic",
    "Bug",
    "Rock",
    "Ghost",
    "Dragon",
    "Dark",
    "Steel",
    "Fairy",
    name="pokemon_types",
)


# Defining the Pokemon model
class Pokemon(db.Model):
    """
    This class represents a Pokemon in the database.
    """

    # setting the table name
    __tablename__ = "pokemons"

    # Defining model attributes (columns)
    id: Mapped[int] = mapped_column(primary_key=True)
    # Primary key for the table

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # Pokemon name (string, not nullable)

    type: Mapped[str] = mapped_column(pokemon_types, nullable=False)
    # Pokemon type (uses the 'pokemon_types' Enum)

    ability: Mapped[str] = mapped_column(String(100), nullable=False)
    # Pokemon ability (string, not nullable)

    date_caught: Mapped[date]
    # Date the Pokemon was caught

    trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.id"), nullable=True)
    # Foreign key referencing the 'trainers' table

    trainer: Mapped["Trainer"] = relationship(back_populates="pokemons")
     # Relationship with the 'Trainer' model

# Defining the PokemonSchema for serialisation and validation
class PokemonSchema(ma.Schema):
    """
    This class defines the Marshmallow schema for the Pokemon model.
    It specifies how Pokemon objects are serialised and validated.
    """
    name = fields.String(
        validate=[
            Regexp(
                "^[a-zA-Z]+$",
                error="Pokemon name must contain only letters.",
            ),
        ],
        required=True,
    )
    trainer = fields.Nested(
        "TrainerSchema", exclude=["password", "admin", "id", "email"], allow_none=True
    )

    class Meta:
        fields = ("id", "name", "type", "ability", "date_caught", "trainer")
