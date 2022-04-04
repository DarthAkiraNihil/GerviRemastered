class Throwable:
    def __init__(self, name, level, msgTemplate):
        self.name = name
        self.level = level
        self.msgTemplate = msgTemplate
    def throw(self, *args):
        msg = msg % (args)
        return '%s [%s]: %s' % (self.name, self.level, msg)