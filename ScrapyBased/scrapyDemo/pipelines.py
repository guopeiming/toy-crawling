# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class MyPipeline:

    def __init__(self) -> None:
        self.file = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def open_spider(self, spider):
        self.file = open('./items.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(self._item_cleaning(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def _item_cleaning(self, item):
        article: str = item['article']
        article = article.replace('\xa0', '')
        item['article'] = article
        return item
