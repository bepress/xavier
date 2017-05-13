import threading

thread_data = threading.local()
thread_data.brain = None


def register_brain(brain):
    thread_data.brain = brain


def get_active_brain():
    return thread_data.brain


def unregister_brain():
    thread_data.brain = None
