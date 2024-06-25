from datetime import timedelta
from flask import Blueprint, request, abort
from sqlalchemy import and_
from flask_jwt_extended import create_access_token
from init import db, bcrypt
from models.trainer import Trainer, TrainerSchema
from auth import admin_only

# Prefixing the URL for the 'trainers' blueprint with '/trainers' to route related endpoints
trainers_bp = Blueprint("trainers", __name__, url_prefix="/trainers")


@trainers_bp.route("/login", methods=["POST"])
def login():
    # get the email and password from the request
    params = TrainerSchema(only=["username", "email", "password"]).load(
        request.json, unknown="exclude"
    )
    stmt = db.select(Trainer).where(and_(Trainer.email == params["email"], Trainer.username == params["username"]))
    trainer = db.session.scalar(stmt)
    if trainer and bcrypt.check_password_hash(trainer.password, params["password"]):
        # Generate the JWT
        token = create_access_token(
            identity=trainer.id, expires_delta=timedelta(hours=8)
        )
        # now we return the JWT
        return {"token": token}
    else:
        # Error handling if trainer is not found, wrong username or wrong password)
        return abort(401, description="Invalid username, email or password")
