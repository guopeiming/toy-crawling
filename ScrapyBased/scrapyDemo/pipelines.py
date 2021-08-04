# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import logging

class MyPipeline:

    def __init__(self, host, port, database, user, passwd) -> None:
        self.db_conn =pymysql.connect(host=host, port=port, database=database, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()

        self.logger = logging.getLogger(__name__)
        msg = "Conneting to mysql: %(host)s:%(port)d %(database)s"
        args = {'host': host, 'port': port, 'database': database}
        self.logger.info(msg, args)

        self.cached_urls = None

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get('MYSQL_HOST', 'localhost')
        port = crawler.settings.get('MYSQL_PORT', 6761)
        datebase = crawler.settings.get('MYSQL_DB_NAME','crawling_db')
        user = crawler.settings.get('MYSQL_USER', 'root')
        passwd = crawler.settings.get('MYSQL_PASSWORD', 'mysql')
        return cls(host, port, datebase, user, passwd)

    def open_spider(self, spider):
        self.cached_urls = self.__load_urls_cached(spider.get_source_site())

    def close_spider(self, spider):
        self.db_cur.close()
        self.db_conn.close()

    def process_item(self, item, spider):
        item = self._item_cleaning(item)
        if item['url'] not in self.cached_urls:
            self.insert_db(item)
        return item

    def _item_cleaning(self, item):
        article: str = item['article']
        article = article.replace('\xa0', '')
        item['article'] = article[:2000]
        return item

    def insert_db(self, item):
        values = (
            item['source_site'],
            item['url'],
            item['article'],
            item['create_time'],
        )
        try:
            sql = 'INSERT INTO articles (source_site, url, article, create_time) VALUES(%s, %s, %s, %s);'
            self.db_cur.execute(sql, values)
            self.db_conn.commit()
        except Exception as e:
            self.db_conn.rollback()
            msg = ('Mysql error: %s. sql: ' + sql) % ((str(e),)+ values)
            self.logger.warning(msg)

    def __load_urls_cached(self, source_site):
        urls = set()
        try:
            sql = 'select url FROM articles WHERE source_site = %s'
            self.db_cur.execute(sql, (source_site, ))
        except Exception as e:
            msg = ('Mysql error: %s. sql: ' + sql) % ((str(e), source_site))
            self.logger.warning(msg)
        else:
            for data in self.db_cur.fetchall():
                urls.add(data['url'])
        return urls
