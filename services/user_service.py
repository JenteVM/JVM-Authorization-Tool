from flask import abort
from models.user_model import UserModel
from utils.db_utils import db, connect_with_user_db, generate_user_id, generate_auth_token
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def create_user(db_id:str, username, password, email=None, auth_level="user"): #creates a new user in the specified database
    db, app = connect_with_user_db(db_id)
    with app.app_context():
        if email:
            if UserModel.query.filter_by(email=email).first():
                abort(400, description="Email has already been registered.")
        if UserModel.query.filter_by(username=username).first():
            abort(400, description="Username has already been taken.")
    
        hashed_password = generate_password_hash(password)
        new_user = UserModel(
            user_id=generate_user_id(),
            username=username if username else None,
            email=email if email else None,
            password_hash=hashed_password,
            auth_level=auth_level,
            creation_date=datetime.now(),
        )

        db.session.add(new_user)
        db.session.commit()
        print(new_user) #required to avoid lazy loading issues (detached instance)
        return new_user

def get_all_users(db_id:str): #returns all users in the specified database
    db, app = connect_with_user_db(db_id)
    if not db:
        abort(404, description="Database not found.")
    with app.app_context():
        users = UserModel.query.all()
        return users

def get_user_by(db_id:str, id_method:str, identifier:str): #returns a user from a specific database by the specified method and identifier
    db, app = connect_with_user_db(db_id)
    if not db:
        abort(404, description="Database not found.")
    with app.app_context():
        if id_method == "id":
            user = UserModel.query.filter_by(user_id=identifier).first()
            if not user:
                return None
            return user
    
        elif id_method == "username":
            user = UserModel.query.filter_by(username=identifier).first()
            if not user:
                return None
            return user
       
        elif id_method == "email":
            user = UserModel.query.filter_by(email=identifier).first()
            if not user:
                return None
            return user
        
        else:
            abort(404, description="Method not found.")

def update_user(db_id, identifier, username=None, email=None, password=None, time_extension=None): #updates a user in the specified database
    db, app = connect_with_user_db(db_id)
    with app.app_context():
        user = UserModel.query.filter_by(user_id=identifier).first()
        try:
            db.session.delete(user)
            if not user:
                abort(404, description="User not found")
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.password_hash = generate_password_hash(password)
            if time_extension:
                user.auth_token = generate_auth_token()
                if not user.auth_token_expiration or user.auth_token_expiration < datetime.now():
                    user.auth_token_expiration = datetime.now() + timedelta(minutes=time_extension)
                else:
                    user.auth_token_expiration = user.auth_token_expiration + timedelta(minutes=time_extension)
            db.session.add(user)
            db.session.commit()
            print(user) #required to avoid lazy loading issues (detached instance)
        except Exception as e:
            db.session.rollback()
            print(e)
            abort(500)
        return user
    
def delete_user(db_id, method, value): #deletes a user from the specified database
    db, app = connect_with_user_db(db_id)
    with app.app_context():
        user = get_user_by(method,value)
        if not user:
            abort(404, description="User not found.")
        db.session.delete(user)
        return {"message":"User deleted succesfully."}

def validate_auth_token(db_id, token): #checks if the user has a valid auth token
    db, app = connect_with_user_db(db_id)
    with app.app_context():
        user = UserModel.query.filter_by(auth_token=token).first()
        if not user:
            return False
        return True