from flask import Blueprint, current_app
from flaskr.cache import cache
from flask import request
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('cwral', __name__)


@bp.route('/hello')
def hello():
    return 'hello'


@bp.route('/cwral')
def cwral():
    ret = dict()
    status = 200
    try:
        site = request.args.get('site')
        if site not in current_app.config['SITES_LIST']:
            raise ValueError()
    except:
        logger.warning('error request args: %s' % str(request.args))
        ret['err_msg'] = 'error site'
        status = 400
    else:
        if cache.get(site):
            ret['err_msg'] = 'Cwraling'
            status = 403
        else:
            ret['msg'] = 'start cwraling'
            cache.set(site, True)
    return ret, status
