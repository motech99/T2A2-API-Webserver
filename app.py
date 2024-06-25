from flask import jsonify
from init import app
from blueprints.cli_bp import db_commands
from blueprints.trainers_bp import trainers_bp

app.register_blueprint(db_commands)
app.register_blueprint(trainers_bp)


@app.route('/')
def index():
    return "Pokemon!"

@app.errorhandler(404)
def not_found(err):
    return jsonify({"error": "Not Found"}), 404