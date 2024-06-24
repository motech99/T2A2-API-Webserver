from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt



# used to define classes mapped to relational database tables
class Base(DeclarativeBase):
    pass

app = Flask(__name__)


## DB CONNECTION
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)