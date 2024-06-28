from flask import jsonify
from marshmallow.exceptions import ValidationError
from init import app
from blueprints.cli_bp import db_commands
from blueprints.trainers_bp import trainers_bp
from blueprints.pokemons_bp import pokemons_bp

# Register blueprints with the Flask application
app.register_blueprint(db_commands)
app.register_blueprint(trainers_bp)
app.register_blueprint(pokemons_bp)


# Error handler for 404 (Not Found) and 405 (Method Not Allowed) errors
@app.errorhandler(404)
@app.errorhandler(405)
def not_found():
    """Returns a JSON response with an 'error' message for 404 and 405 errors"""
    return jsonify({"error": "Not Found"}), 404

# Error handler for ValidationError (invalid data)
@app.errorhandler(ValidationError)
def invalid_request(err):
    """Returns a JSON response with validation error messages for ValidationError"""
    return jsonify({"error": vars(err)["messages"]}), 400

# Specific error handler for 404 None (Not Found) errors
@app.errorhandler(404)
def not_found_error(error=None):
    """Returns a JSON response with a more informative 'error' message for 404"""
    error_message = "Not Found" if error is None else str(error)
    return jsonify({"error": error_message}), 404