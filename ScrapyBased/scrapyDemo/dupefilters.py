from scrapy.dupefilters import BaseDupeFilter, referer_str
import logging
import hashlib
from scrapy.utils.python import to_bytes


class MyRFPDupeFilter(BaseDupeFilter):
    """My Request Fingerprint duplicates filter"""

    def __init__(self, debug=False):
        self.fingerprints = set()
        self.logdupes = True
        self.debug = debug
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(debug)

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)

    def request_fingerprint(self, request) -> str:
        return hashlib.md5(to_bytes(request.url)).hexdigest()

    def close(self, reason):
        msg = "The number of URLs: %(url_num)d"
        args = {'url_num': len(self.fingerprints)}
        self.logger.info(msg, args)

    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s (referer: %(referer)s)"
            args = {'request': request, 'referer': referer_str(request)}
            self.logger.debug(msg, args, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)
