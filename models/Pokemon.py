from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, ForeignKey
from marshmallow import fields
from marshmallow.validate import Regexp
from init import db, ma

# Creating pokemon types
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


class Pokemon(db.Model):
    # setting the table name
    __tablename__ = "pokemons"

    # creating Columns, IDs are always primary keys
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(pokemon_types, nullable=False)
    ability: Mapped[str] = mapped_column(String(100), nullable=False)
    date_caught: Mapped[date]

    trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.id"), nullable=True)
    trainer: Mapped["Trainer"] = relationship(back_populates="pokemons")


# Creating a Marshmallow Schema to serialise and validate SQLAlchemy Models
class PokemonSchema(ma.Schema):
    name = fields.String(
        validate=[
            Regexp(
                "^[a-zA-Z]+$",
                error="Pokemon name must contain only letters.",
            ),
        ],
        required=True,
    )
    trainer = fields.Nested("TrainerSchema", exclude=["password"])

    class Meta:
        fields = ("id", "name", "type", "ability", "date_caught")
