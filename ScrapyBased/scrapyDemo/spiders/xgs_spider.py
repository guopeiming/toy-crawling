import time
from typing import List
import scrapy
from scrapy.http import HtmlResponse


class XGSSpider(scrapy.Spider):

    name = 'xgs'
    allowed_domains = [
        'www.iie.cas.cn'
    ]
    start_urls = [
        'http://www.iie.cas.cn/',
    ]

    def parse(self, response: HtmlResponse):
        if response.url.endswith('.html'):
            article = self._parse_article(response)
            if len(article) > 0:
                yield {
                    'article': article, 'source_site': 'http://www.iie.cas.cn/',
                    'url': response.headers.url,
                    'create_time': time.strftime('%Y-%m-%d %H:%M:%S')
                }

        page_links = response.xpath(
            # '//a[not(contains(@href, ".pdf")) and not(contains(@href, ".doc")) and \
            #      not(starts-with(@href, "mailto:")) and not(contains(@href, ".jpg")) and \
            #      not(contains(@href, ".rar")) and not(contains(@href, "javascript"))]'
            '//a[not(starts-with(@href, "mailto:")) and not(contains(@href, "javascript"))]'
        )
        yield from response.follow_all(page_links, callback=self.parse)

    def _parse_article(self, response: HtmlResponse):
        article = ''
        raw_article: List[str] = response.xpath(
            '//div[@id="xlmain"]//*[name(.)!="style" and name(.)!="script" and name(.)!="img"]/text()'
        ).getall()

        if len(raw_article) > 0:
            for span in raw_article:
                article += span.strip()
        return article
