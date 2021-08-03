from flask import Blueprint, current_app
from flaskr.utils import MyCache, MyExecutor
from flask import request
import requests
import logging
from time import sleep

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
        if MyCache.get(site):
            ret['err_msg'] = 'Cwraling'
            status = 403
        else:
            ret['msg'] = 'start cwraling'
            MyCache.set(site, True)
            MyExecutor.init_executor()
            MyExecutor.submit(cwral_task, site)
            MyExecutor.shutdown(False)
    return ret, status


@bp.route('/end')
def end():
    site = request.args.get('site')
    MyCache.delete(site)
    return {'msg': 'OK'}, 200


def cwral_task(site):
    sleep(5)
    print("Task is done!")
    res = requests.get('http://127.0.0.1:5000/end?site='+site)
