##
# Subclass threading.Thread to pass through arguments as well
# @author Patrick Kage

import threading

class ArgThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        # super call
        threading.Thread.__init__(self,
                                  group=group,
                                  name=name)
        self.args = args
        self.kwargs = kwargs
        self.target = target

    def run(self):
        self.target(*self.args, **self.kwargs)
