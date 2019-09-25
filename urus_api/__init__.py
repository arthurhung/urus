import os
from flask import Flask
from flask import Blueprint
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from urus_api.utility import utility_logger
from urus_api.utility import middleware

db = SQLAlchemy()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app(config_obj=None):
    # create and configure the app
    app = Flask(__name__)
    # app.wsgi_app = middleware.ClientRequestDataRecordMiddleware(app.wsgi_app)
    db.init_app(app)

    if config_obj:
        config_dict = dict(
            [(k, getattr(config_obj, k)) for k in dir(config_obj) if not k.startswith('_')])
        app.config.update(config_dict)
    api_version = config_dict.get("API_VERSION", "")
    swagger_config = {
        "headers": [],
        "info": {
            "title": "Urus API docs",
            "version": api_version,
            "description": "### By Arthur",
            "contact": {
                "email": "arthur.hung@sinopac.com"
            }
        },
        "host":
            config_dict.get("HTTPS_DOMAIN", config_dict.get("DOMAIN")),
        "schemes": ["http", "https"],
        "bashPath":
            f"/Urus/{api_version}",
        "specs": [{
            "endpoint": 'apispec',
            "route": '/Urus/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }],
        # "static_url_path":
        #     "/flasgger_static",
        "static_folder":
            BASE_DIR + "/urus_api/flasgger_static",  # must be set by user
        "swagger_ui":
            True,
        "specs_route":
            "/Urus/apidocs/"
    }

    Swagger(app, config=swagger_config)
    # if config_obj is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(config_name)

    # Register blueprint(s)
    from urus_api.v1.ris_gov.urls import gov_bp
    from urus_api.v1.line_broadcast.urls import line_broadcast_bp

    app.register_blueprint(gov_bp)
    app.register_blueprint(line_broadcast_bp)

    return app