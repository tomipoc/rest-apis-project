import os
import secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from blocklist import BLOCKLIST
import models  # the same as import models.__init__

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    
    # configs for flask and flask-smorest
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" # loads swagger code from somewhere
    
    # db settings
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.sqlite")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    
    api = Api(app)
    
    # config JWT
    app.config["JWT_SECRET_KEY"] = "307135097899575159263580899543983432664"  # run python from terminal, import secrets, secrets.SystemRandom().getrandbits(128)
    jwt = JWTManager(app)
    
    # for logout
    
    # whenever we receive a jwt, this function runs
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
        # if this function returns true, then the request is terminated
        # and the user will get an error: the token has been revoked/not avilable
    
    # based on the previous function (check_if_token_in_blocklist)
    # in case of false it will be returned
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token has been revoked.", "error": "token_revoked"}), 401, )
    
    @jwt.needs_fresh_token_loader
    def doken_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token is not fresh.", "error": "fresh_token_required"}), 401)
    
    # JWT claim
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1: # it should look in a db and check if user is admin
            return {"is_admin": True}
        return {"is_admin": False}
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({"message": "The token has expired.", "error": "token_expired"}), 401, )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return ( jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401, )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return ( jsonify({"description": "Request does not contain an access token.", "error": "authorization_required",}), 401, )
    
    # @app.before_first_request
    # def create_tables():
    #     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
