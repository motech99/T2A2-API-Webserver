from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import abort, jsonify, make_response
from init import db
from models.trainer import Trainer


# Route decorator to ensure JWT trainer is an admin
def admin_only(fn):
    @jwt_required()
    def inner():
        trainer_id = get_jwt_identity()
        stmt = db.select(Trainer).where(Trainer.id == trainer_id, Trainer.admin)
        trainer = db.session.scalar(stmt)
        if trainer:
            return fn()
        else:
            return {'error': 'You need to have administrator privileges to access this resource'}, 403
        
    return inner

# Ensure that the JWT trainer is the owner of the given pokemon
def authorize_owner_pokemon(pokemon):
    trainer_id = get_jwt_identity()
    if trainer_id != pokemon.trainer_id:
        abort(make_response(jsonify(error="You must be the pokemon owner to access this resource"), 403))


def authorize_owner_trainer(trainer):
    trainer_id = get_jwt_identity()
    if trainer_id != trainer.id:
        abort(make_response(jsonify(error="You must be a registered trainer to access this resource"), 403))
