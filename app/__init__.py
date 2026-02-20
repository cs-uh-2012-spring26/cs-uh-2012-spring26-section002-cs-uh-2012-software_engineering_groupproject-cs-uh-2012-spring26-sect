from app.apis.hello import api as hello_ns
from app.apis.classes import api as classes_ns
from app.apis.auth import api as auth_ns
from app.apis.bookings import api as bookings_ns
from app.config import Config
from app.db import DB

from http import HTTPStatus
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    DB.init_app(app)
    
    jwt = JWTManager(app)

    api = Api(
        title="Fitness Class API",
        version="1.0",
        description="Backend API for fitness class management",
    )

    api.init_app(app)

    api.add_namespace(hello_ns)
    api.add_namespace(classes_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(bookings_ns)

    @api.errorhandler(Exception)
    def handle_input_validation_error(error):
        return {"message": str(error)}, HTTPStatus.INTERNAL_SERVER_ERROR

    return app
