import json
from collections import defaultdict
from functools import wraps

from routes import Mapper


def cors_response(*args, **kwargs):
    return Response(200, {}, {
        "Access-Control-Allow-Origin": "*"
    })


class Router(object):
    def __init__(self):
        self.mappers = defaultdict(lambda: Mapper())

    def find_route(self, path, method='GET'):
        method = method.upper()
        return self.mappers[method].match(path)

    def _add_route(self, path, method, view, cors=False, **kwargs):
        kwargs['view'] = view
        kwargs['cors'] = cors
        self.mappers[method].connect(None, path, **kwargs)

    def add_route(self, path, methods=['GET'], **kwargs):

        def outside(func):

            for method in methods:
                self._add_route(path, method, func, **kwargs)

            if kwargs.get('cors'):
                self._add_route(path, "OPTIONS", cors_response)

            @wraps(func)
            def __wrapper(*args, **kwargs):
                return func(*args, **kwargs)

        return outside


class HTTPError(Exception):
    def __init__(self, message, slug, status_code):
        self.message = message
        self.slug = slug
        self.status_code = status_code


class Response(object):
    def __init__(self, status_code, body, headers=None):
        self.headers = {
            'Content-Type': "application/json",
        }

        if headers:
            self.headers.update(headers)

        self.status_code = status_code
        self.body = body

    def render(self):
        return json.dumps(self.body)
