from flask_restful import Resource, reqparse, fields, marshal_with
from services.registry_service import create_registry_entry, get_registry_entry_by_id, get_registry_entries, get_allowed_origins, patch_registry_entry, check_post_level_auth
from utils.db_utils import generate_AO_addition_token
from flask import request, abort

registry_args = reqparse.RequestParser()
registry_args.add_argument("app_name", type=str, required=True, help="App name is required.")
registry_creation_fields = {
    "db_id": fields.String,
    "app_name": fields.String,
    "allowed_origins": fields.String,
    "AO_addition_token": fields.String,
    "authorized": fields.Boolean,
}
registry_limited_fields = {
    "db_id": fields.String,
    "app_name": fields.String,
    "authorized": fields.Boolean,
}
AO_addition_token_fields = {
    "AO_addition_token": fields.String,
    "message": fields.String,
}

class RegistryListResource(Resource): #queries all registry entries and allows creation of new entries
    @marshal_with(registry_limited_fields)
    def get(self):
        return get_registry_entries()

    @marshal_with(registry_creation_fields)
    def post(self):
        ALLOWED_REGISTRY_CREATORS = get_allowed_origins(partial=True)
        origin = request.headers.get("Origin")
        if origin not in ALLOWED_REGISTRY_CREATORS:
            abort(403, description="Unauthorized Origin.")
        args = registry_args.parse_args()
        app_name = args["app_name"]
        new_entry = create_registry_entry(app_name)
        return new_entry, 201

class RegistryLookupResource(Resource): #queries a singular registry instance
    @marshal_with(registry_limited_fields)
    def get(self, db_id):
        entry = get_registry_entry_by_id(db_id)
        if entry:
            return entry, 200
        abort(404, description="Database not found.")

class RegistryAuthenticateResource(Resource): #adds allowed origins to a registry entry if it has a valid token
    @marshal_with(AO_addition_token_fields)
    def get(self, db_id, token):
        entry = get_registry_entry_by_id(db_id)
        if not entry:
            abort(404, description="db instance not found.")
        if not entry.allowed_origins:
            entry.allowed_origins = request.headers.get("Origin")
        else:
            entry.allowed_origins = entry.allowed_origins + "," + request.headers.get("Origin")
        if entry.AO_addition_token and entry.AO_addition_token == token:
            patch_registry_entry(db_id, AO_addition_token=None, allowed_origins=entry.allowed_origins)
            return {"message": "Allowed origin added successfully."}, 200
        elif token == "create":
            if not check_post_level_auth(db_id):
                abort(403, description="Unauthorized Origin.")
            user = patch_registry_entry(db_id, AO_addition_token=generate_AO_addition_token())
            return user, 200
        else:
            abort(403, description="Invalid token.")