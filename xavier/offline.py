from functools import wraps
import logging
import pickle

logger = logging.getLogger(__name__)


class BackgroundTask(object):
    def __init__(self, func, publish_event):
        self.func = func
        self.path = '%s.%s' % (func.__name__, func.__module__)
        self.publish_event = publish_event

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def delay(self, *args, **kwargs):
        event = pickle.dumps((self.path, args, kwargs))
        self.publish_event(event)

        return True


class BackgroudQueue(object):
    def __init__(self, publish_event):
        self.functions = {}
        self.publish_event = publish_event

    def process_event(self, event):
        name, args, kwargs = pickle.loads(event)

        func = self.functions.get(name)
        if not func:
            logger.info("processing event - missing function name: %s", name)

        try:
            func(*args, **kwargs)
        except Exception as e:
            return False

        return True

    def task(self, func):

        func = BackgroundTask(func, self.publish_event)
        self.functions[func.path] = func
        return func
