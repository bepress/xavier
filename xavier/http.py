import json

from functools import wraps

from routes import Mapper


class Router(object):
    def __init__(self):
        self.mapper = Mapper()

    def find_route(self, path):
        return self.mapper.match(path)

    def add_route(self, path, methods=['GET'], **kwargs):

        def outside(func):

            conditions = kwargs.get('conditions', {})
            conditions.update({
                'methods': methods
            })
            kwargs['conditions'] = conditions
            kwargs['view'] = func
            self.mapper.connect(None, path, **kwargs)

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
