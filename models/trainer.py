from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean
from init import db, ma


class Trainer(db.Model):
    __tablename__ = "trainers"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(200))
    username: Mapped[str] = mapped_column(Text(), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    admin: Mapped[bool] = mapped_column(Boolean(), server_default="false")


class TrainerSchema(ma.Schema):
    
    class Meta:
        fields = ("id", "name", "username", "password")
