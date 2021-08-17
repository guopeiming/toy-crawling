from flask import Blueprint, current_app
from flaskr.utils import MyDB, MyExecutor
from flask import request
import hashlib
import logging
import time
import os
import random

logger = logging.getLogger(__name__)

bp = Blueprint('crawl', __name__)


@bp.route('/hello')
def hello():
    return 'hello'


@bp.route('/crawl/<site>', methods=['GET', 'POST'])
def crawl(site):
    ret = dict()
    status = 200

    if site not in current_app.config['SITES_DICT']:
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
        MyExecutor.submit(
            crawl_task, current_app.config['SCRAPY_PATH'],
            current_app.config['SITES_DICT'][site], hashcode
        )
        MyExecutor.shutdown(False)

        mydb = MyDB()
        mydb.insert(hashcode, 'crawling')
        mydb.close()
    return ret, status


def crawl_task(path, site, hashcode):
    command = 'cd %s && scrapy crawl %s --logfile=./%s.log -a crawler_id=%s'%(path, site, hashcode, hashcode)
    print('start crawling. command: '+command)
    returncode = os.system(command)
    print('crawling finished. returncode: %d. hashcode: %s.'%(returncode, hashcode))


@bp.route('/status/<id_>', methods=['GET', 'POST'])
def status(id_):
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
