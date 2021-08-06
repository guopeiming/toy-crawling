import logging
from flask_caching import Cache
from flask import current_app
from concurrent.futures import ThreadPoolExecutor
import pymysql
import logging


logger = logging.getLogger(__name__)

class MyExecutor:
    __executor = None

    @classmethod
    def init_executor(cls):
        cls.__executor = ThreadPoolExecutor(2)

    @classmethod
    def submit(cls, *args, **kwargs):
        return cls.__executor.submit(*args, **kwargs)

    @classmethod
    def shutdown(cls, *args):
        return cls.__executor.shutdown(*args)


class MyDB:

    def __init__(self) -> None:
        self.conn = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DB_NAME'],
                port=current_app.config['MYSQL_PORT'],
                charset='utf8',
            )
        self.cur = self.conn.cursor()

    def insert(self, crawler_id, status):
        try:
            sql = 'INSERT into crawlers (crawler_id, status) values (%s, %s);'
            values = (crawler_id, status)
            self.cur.execute(sql, values)
            self.conn.commit()
        except:
            self.conn.rollback()
            logger.warning('DB insert error: ' + (sql % values))
        else:
            logger.info('DB inserting succeeds: %s'%crawler_id)

    def query(self, crawler_id):
        try:
            sql = 'select status from crawlers where crawler_id = %s'
            self.cur.execute(sql, (crawler_id, ))
            data = self.cur.fetchone()
            if data:
                return data[0]
            else:
                return 'error id'
        except:
            logger.warning('DB query error, sql: ' + (sql % crawler_id))
            return 'DB query error'

    def close(self):
        self.cur.close()
        self.conn.close()


class MyCache:
    __cache = Cache()

    @classmethod
    def init_cache(cls):
        cls.__cache.init_app(current_app)

    @classmethod
    def get(cls, *args, **kwargs):
        return cls.__cache.get(*args, **kwargs)

    @classmethod
    def set(cls, *args, **kwargs):
        return cls.__cache.set(*args, **kwargs)

    @classmethod
    def delete(cls, *args, **kwargs):
        return cls.__cache.delete(*args, **kwargs)
