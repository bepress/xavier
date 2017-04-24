import json


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
