from flask import Blueprint, current_app
from flaskr.utils import MyDB, MyExecutor
from flask import request
import hashlib
import logging
from time import sleep
import time
import random

logger = logging.getLogger(__name__)

bp = Blueprint('crawl', __name__)


@bp.route('/hello')
def hello():
    return 'hello'


@bp.route('/crawl')
def crawl():
    ret = dict()
    status = 200
    site = request.args.get('site')
    if site not in current_app.config['SITES_LIST']:
        logger.warning('error request args: %s' % str(request.args))
        ret['msg'] = 'error site'
        status = 400
    else:
        ret['msg'] = 'start crawling'
        string = site + str(time.time()) + str(random.random)
        hashcode = hashlib.md5(string.encode()).hexdigest()
        ret['id'] = hashcode
        ret['time'] = '5 min'
        MyExecutor.init_executor()
        MyExecutor.submit(crawl_task, site, hashcode)
        MyExecutor.shutdown(False)
        mydb = MyDB()
        mydb.insert(hashcode, 'crawling')
        mydb.close()
    return ret, status


def crawl_task(site, hashcode):
    sleep(5)
    print(hashcode, site)
    print("Task is done!")


@bp.route('/status')
def status():
    id_ = request.args.get('id')
    mydb = MyDB()
    res = mydb.query(id_)
    mydb.close()
    if res == 'error id':
        status_code = 403
    elif res == 'DB query error':
        status_code = 500
    else:
        status_code = 200
    return {'msg': res}, status_code
