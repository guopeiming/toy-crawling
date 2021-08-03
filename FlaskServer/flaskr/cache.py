from flask_caching import Cache
from flask import current_app


cache = Cache()


def init_cache():
    cache.init_app(current_app)
