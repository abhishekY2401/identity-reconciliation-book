from app.database import db
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from app.api.reconciliation_api import reconciliation


# application factory pattern


def create_app():
    app = Flask(__name__)

    # setup flask app config
    app.config.from_object('app.config.DevelopmentConfig')

    # initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    CORS(app)

    app.register_blueprint(reconciliation)

    return app
