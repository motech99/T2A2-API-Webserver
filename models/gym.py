from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum
from init import db, ma

# Creating gym types
gym_types = Enum(
    "Mystic",
    "Valor",
    "Instinct",
    name="gym_types",
)

class Gym(db.Model):
    # setting the table name
    __tablename__ = "gyms"

    # creating Columns, IDs are always primary keys
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    team: Mapped[str] = mapped_column(gym_types, nullable=False)


# Creating a Marshmallow Schema to serialise and validate SQLAlchemy Models
class GymSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "team")
