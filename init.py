from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


# used to define classes mapped to relational database tables
class Base(DeclarativeBase):
    pass


app = Flask(__name__)


## DB CONNECTION
app.config["JWT_SECRET_KEY"] = environ.get("JWT_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URI")


# Initialise SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Bind SQLAlchemy to the Flask app
db.init_app(app)

# Initialise Marshmallow for object serialisation/deserialisation
ma = Marshmallow(app)

# Initialise Bcrypt for password hashing
bcrypt = Bcrypt(app)

# initalise JWTManager
jwt = JWTManager(app)
