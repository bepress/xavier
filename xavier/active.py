import threading

thread_data = threading.local()
thread_data.bot = None


def register_bot(bot):
    thread_data.bot = bot


def get_active_bot(bot):
    return thread_data.bot


def unregister_bot():
    thread_data.bot = None
