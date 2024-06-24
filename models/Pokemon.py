from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum
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
    # setting the tablename name
    __tablename__ = "pokemons"

    # creating Columns, IDs are always primary keys
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(pokemon_types, nullable=False)
    ability: Mapped[str] = mapped_column(String(100), nullable=False)
    date_caught: Mapped[date]


# Creating a Marshmallow Schema to serialise and validate SQLAlchemy Models
class PokemonSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "type", "ability", "date_caught")
