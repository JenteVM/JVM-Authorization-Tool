import os
import secrets
import uuid
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()
app = Flask(__name__)
from models.registry_models import RegistryModel

def get_db_uri(db_secret): #returns the db location
    instance_path = os.path.join(os.getcwd(), "instance")
    db_path = os.path.join(instance_path, db_secret)
    return f"sqlite:///{db_path}.db"

def generate_ids(): #generates a db_id and db_secret for a new database
    db_id = secrets.token_urlsafe(8)
    db_secret = str(uuid.uuid4())
    return db_id, db_secret

def generate_user_id(): #generates a user_id for a new user
    return secrets.token_hex(16)

def create_user_db(db_secret): #creates a running db instance to handle requests
    db_uri = get_db_uri(db_secret)
    create_user_db_app = Flask(__name__)
    create_user_db_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    create_user_db_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(create_user_db_app)
    try:
        with create_user_db_app.app_context():
            db.create_all()
        return True
    except SQLAlchemyError as err:
        print(f"[DB Creation Error] {err}")

def connect_with_user_db(db_id): #connects with a db created using create_user_db
    data = RegistryModel.query.filter_by(db_id=db_id).first()
    db_secret = data.db_secret
    connect_with_user_db_app = Flask(__name__)
    connect_with_user_db_app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri(db_secret)
    connect_with_user_db_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(connect_with_user_db_app)
    return db, connect_with_user_db_app