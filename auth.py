from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.trainer import Trainer


# Route decorator to ensure JWT user is an admin
def admin_only(fn):
    @jwt_required()
    def inner():
        trainer_id = get_jwt_identity()
        stmt = db.select(Trainer).where(Trainer.id == trainer_id, Trainer.admin)
        trainer = db.session.scalar(stmt)
        if trainer:
            return fn()
        else:
            return {'error': 'You need to have administrator privileges to access this resource.'}, 403
        
    return inner