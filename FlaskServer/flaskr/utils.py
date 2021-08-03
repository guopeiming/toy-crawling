from flask_caching import Cache
from flask import current_app
from concurrent.futures import ThreadPoolExecutor


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
