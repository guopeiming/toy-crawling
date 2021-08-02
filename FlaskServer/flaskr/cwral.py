from flask import Blueprint, current_app


bp = Blueprint('cwral', __name__)


# a simple page that says hello
@bp.route('/hello')
def hello():
    return current_app.config['SITES_LIST'][0]
