from typing import Dict
from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=False)

    from . import crawl
    app.register_blueprint(crawl.bp)


    return app
