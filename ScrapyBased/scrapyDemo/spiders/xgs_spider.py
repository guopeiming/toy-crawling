from typing import List
import scrapy


class XGSSpider(scrapy.Spider):

    name = 'xgs'
    allowed_domains = [
        'http://www.iie.cas.cn'
    ]
    start_urls = [
        'http://www.iie.cas.cn'
    ]

    def parse(self, response):
        article = ''
        raw_article: List[str] = response.xpath(
            '//div[@id="xlmain"]//*[name(.)!="style" and name(.)!="script" and name(.)!="img"]/text()'
        )

        if len(raw_article) > 0:
            for i, span in enumerate(raw_article):
                article += span.strip()
                if i == 0 or i == 2:
                    article += '。'
            yield {'article': article}

        page_links = response.xpath('//a')
