import types


class Range:

    start: int
    stop: int
    step: int
    
    def __init__(self, *args):
        if len(args) == 1:
            self._init1(*args)
        else:
            self._init2(*args)

    def _init1(self, stop: int):
        self.start = 0
        self.step = 1
        self.stop = stop
    
    def _init2(self, start: int, stop: int, step: int = 1):
        self.start = start
        self.step = step
        self.stop = stop

    def __iter__(self):
        idx = self.start
        while idx < self.stop:
            yield idx
            idx += self.step
        return
