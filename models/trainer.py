from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean
from marshmallow.validate import Length, Regexp
from marshmallow import fields
from init import db, ma


class Trainer(db.Model):
    __tablename__ = "trainers"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(200))
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    admin: Mapped[bool] = mapped_column(Boolean(), server_default="false")

    pokemons: Mapped[List["Pokemon"]] = relationship(back_populates="trainer")


class TrainerSchema(ma.Schema):
    username = fields.String(
        validate=[
            Length(max=15, error="username cannot be longer than 15 characters!"),
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
        fields = ("id", "name", "email", "username", "password", "admin")
