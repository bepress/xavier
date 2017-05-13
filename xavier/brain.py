
class Brain(object):
    def __init__(self, name='Xavier', env=None):
        self.name = name
        self.env = env if env else {}
