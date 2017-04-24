from functools import wraps

from routes import Mapper


class Bot(object):
    def __init__(self, name='Xavier', env=None):
        self.name = name
        self.env = env if env else {}
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
