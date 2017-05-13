"""
Offline Manager for Xavier

"""
import logging
import jsonpickle

logger = logging.getLogger(__name__)


class Task(object):
    def __init__(self, func, publish_event):
        self.func = func
        self.path = '%s.%s' % (func.__name__, func.__module__)
        self.publish_event = publish_event

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def delay(self, *args, **kwargs):
        event = jsonpickle.dumps((self.path, args, kwargs))
        self.publish_event(event)

        return True

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "BackgroundTask(path='{}')".format(self.path)


class TaskQueue(object):
    def __init__(self, publish_event):
        self.functions = {}
        self.publish_event = publish_event
        self.schedules = {}

    def process_event(self, event):
        name, args, kwargs = jsonpickle.loads(event)

        func = self.functions.get(name)
        if not func:
            logger.info("processing event - missing function name: %s", name)
            raise Exception("Missing function")

        try:
            func(*args, **kwargs)
        except Exception as e:
            return False

        return True

    def process_schedule(self, schedule):
        if schedule not in self.schedules:
            logger.info("Trying to process schedule for unknown schedule: %s", schedule)
            return

        scheduled_functions = self.schedules[schedule]

        logger.info("Running schedule %s registered functions: %s", schedule, scheduled_functions)

        for func in scheduled_functions:
            func.delay()

    def task(self, schedules=None):
        schedules = schedules if schedules else []

        def wrapper(func):
            func = Task(func, self.publish_event)

            self.functions[func.path] = func

            for schedule in schedules:
                if schedule not in self.schedules:
                    self.schedules[schedule] = []

                if func.path not in self.schedules[schedule]:
                    self.schedules[schedule].append(func)

            return func

        return wrapper
