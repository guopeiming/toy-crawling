import os

from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=False)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return app.config['SITES_LIST'][0]

    return app