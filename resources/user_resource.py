from flask_restful import Resource, reqparse, fields, marshal_with
from flask import abort
from services.user_service import get_all_users, get_user_by, create_user, update_user, delete_user, validate_auth_token
from services.registry_service import check_post_level_auth, check_get_level_auth
from werkzeug.security import check_password_hash

user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, required=True, help="Name is required.")
user_args.add_argument("email", type=str)
user_args.add_argument("password", type=str, required=True, help="Password is required.")
user_args.add_argument("auth_level", type=str, default="user")

user_auth_args = reqparse.RequestParser()
user_auth_args.add_argument("username_or_email", type=str, default=None)
user_auth_args.add_argument("password", type=str, default=None)
user_auth_args.add_argument("user_id", type=str, default=None)

user_creation_fields = {
    "user_id": fields.String,
    "username": fields.String,
    "email": fields.String,
    "auth_level": fields.String,
    "creation_date": fields.DateTime,
    "message": fields.String,
}
user_limited_fields = {
    "user_id": fields.String,
    "username": fields.String,
    "email": fields.String,
    "auth_level": fields.String,
    "creation_date": fields.DateTime,
}
auth_token_fields = {
    "user_id": fields.String,
    "auth_level": fields.String,
    "auth_token": fields.String,
    "auth_token_expiration": fields.DateTime,
}

class UserListResource(Resource): #allows all CRUD operations on all of the users (in that database)
    @marshal_with(user_limited_fields)
    def get(self, db_id):
        if not check_get_level_auth(db_id):
            abort(403, description="Unauthorized Origin.")
        return get_all_users(db_id), 200
    
    @marshal_with(user_creation_fields)
    def post(self, db_id):
        if not check_post_level_auth(db_id):
            abort(403, description="Unauthorized Origin.")
        args = user_args.parse_args()
        new_user = create_user(
            db_id,
            username=args["username"],
            email=args["email"],
            password=args["password"],
            auth_level=args["auth_level"],
        )
        return new_user, 201

class UserLookupResource(Resource): #queries a singular user instance
    @marshal_with(user_limited_fields)
    def get(self, db_id, id_method, identifier):
        if not check_get_level_auth(db_id):
            abort(403, description="Unauthorized Origin.")
        user = get_user_by(db_id, id_method, identifier)
        if user is not None:
            return user
        abort(404, description="User not found.")

class UserAuthenticateResource(Resource): #authenticates a user against the database
    @marshal_with(auth_token_fields)
    def post(self, db_id, time_extension:int, token):
        if not check_post_level_auth(db_id):
            abort(403, description="Unauthorized Origin.")
        args = user_auth_args.parse_args()
        if token == "0":
            id_method = "username"
            identifier = args["username_or_email"]
            user = get_user_by(db_id, id_method, identifier)
            if user is not None:
                if check_password_hash(user.password_hash, args["password"]):
                    authorized_user = update_user(db_id, user.user_id, time_extension=time_extension)
                    return authorized_user
                abort(403, description="Invalid credentials.")
            id_method = "email"
            user = get_user_by(db_id, id_method, identifier)
            if user is not None:
                if check_password_hash(user.password_hash, args["password"]):
                    authorized_user = update_user(db_id, user.user_id, time_extension=time_extension)
                    return authorized_user
                abort(403, description="Invalid credentials.")
            abort(404, "User not found")
        else:
            if not validate_auth_token(db_id, token):
                abort(403, description="Invalid or expired token.")
            authorized_user = update_user(db_id, args["user_id"], time_extension=time_extension)
            return authorized_user