from flask import jsonify
from init import app
from blueprints.cli_bp import db_commands
from blueprints.trainers_bp import trainers_bp
from blueprints.pokemons_bp import pokemons_bp
from marshmallow.exceptions import ValidationError

app.register_blueprint(db_commands)
app.register_blueprint(trainers_bp)
app.register_blueprint(pokemons_bp)

@app.route('/')
def index():
    return "Pokemon!"

@app.errorhandler(404)
@app.errorhandler(405)
def not_found():
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(ValidationError)
def invalid_request(err):
    return jsonify({"error": vars(err)["messages"]}), 400


@app.errorhandler(404)
def not_found(error=None):
    # Construct a custom error message or use the default one
    error_message = "Not Found" if error is None else str(error)
    return jsonify({"error": error_message}), 404
