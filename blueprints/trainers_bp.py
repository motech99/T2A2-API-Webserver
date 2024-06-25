from datetime import timedelta
from flask import Blueprint, request, abort
from sqlalchemy import and_, or_
from flask_jwt_extended import create_access_token
from init import db, bcrypt
from models.trainer import Trainer, TrainerSchema
from auth import admin_only

# Prefixing the URL for the 'trainers' blueprint with '/trainers' to route related endpoints
trainers_bp = Blueprint("trainers", __name__, url_prefix="/trainers")


# Trainer Login
@trainers_bp.route("/login", methods=["POST"])
def login():
    # get the username, email and password from the request
    params = TrainerSchema(only=["email", "username", "password"]).load(
        request.json, unknown="exclude"
    )
    # find the trainer by email address and the username
    stmt = db.select(Trainer).where(
        and_(Trainer.email == params["email"], Trainer.username == params["username"])
    )
    trainer = db.session.scalar(stmt)
    # check if trainer is true and the password matches
    if trainer and bcrypt.check_password_hash(trainer.password, params["password"]):
        # Generate the JWT that works for 8 hours
        token = create_access_token(
            identity=trainer.id, expires_delta=timedelta(hours=8)
        )
        # now we return the JWT
        return {"token": token}
    else:
        # Error handling if trainer is not found, wrong username or wrong password)
        return abort(401, description="Invalid username, email or password")


# Get all Trainers (R) (only admin can do this)
@trainers_bp.route("")
@admin_only
def all_trainers():
    # Create a query to fetch all Trainer records
    stmt = db.Select(Trainer)
    trainers = db.session.scalars(stmt).all()

    # Serialise trainers with specified fields and return as JSON
    return TrainerSchema(many=True, only=["id", "name", "username", "email"]).dump(
        trainers
    )


# Get One Trainer (R)
@trainers_bp.route("/<int:id>")
def one_trainer(id):
    # Fetch a Trainer record by ID, raising 404 if not found
    trainer = db.get_or_404(Trainer, id)

    # Serialise trainer with specified fields and return as JSON
    return TrainerSchema(only=["name", "username"]).dump(trainer)


# Create a Trainer (R)
@trainers_bp.route("/create", methods=["POST"])
def create_trainer():
    # Deserialise the requested data, excluding any unknown fields
    trainer_info = TrainerSchema(
        only=["name", "username", "email", "password"], unknown="exclude"
    ).load(request.json)

    # Check for existing username or email
    existing_trainer = db.session.query(Trainer).filter(
        or_(
            Trainer.username == trainer_info["username"],
            Trainer.email == trainer_info["email"],
        )
    ).first()
    if existing_trainer:
        # Raise an error if the trainer already exists
        abort(400, description="This trainer is already registered!")

    # Create a new Trainer object with hashed password
    trainer = Trainer(
        name=trainer_info["name"],
        username=trainer_info["username"],
        email=trainer_info["email"],
        password=bcrypt.generate_password_hash(trainer_info["password"]).decode(
            "utf-8"
        ),
    )
    # Add the new trainer to the database session
    db.session.add(trainer)
    # Commit changes to the database
    db.session.commit()
    # Serialise the newly created trainer and return with 201 successfully Created status
    return TrainerSchema(only=['name','username','email']).dump(trainer), 201
