from g_th import Throwable

class GerviException:
    def __init__(self, name, level, msgTemplate):
        self.throwable = Throwable(name, level, msgTemplate)
    def throw(self, *args):
        self.throwable.throw(args)
