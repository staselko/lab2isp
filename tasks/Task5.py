import inspect
import datetime

def _call_logger(_log, func):
        def packed_func(*args, **kwargs):
            result = func(*args, **kwargs)
            log = """{DateTime} - Called func {func_name}
            Arguments: args:{args_} kwargs{kwargs_}
            Method result: {result}\n""".format(DateTime=datetime.datetime.now().strftime("%Y|%m|%d %H:%M:%S"), 
                                                func_name=func.__name__, args_=args, kwargs_=kwargs, result=result)
            _log.append(log)
            return result
        return packed_func

class Logger(object):
    def __new__(cls, *args, **kwargs):
        obj = super(Logger, cls).__new__(cls, *args, **kwargs)
        obj._log = []
        return obj

    def __getattribute__(self, name: str):
        attribute = super(Logger, self).__getattribute__(name)
        if callable(attribute):
            return _call_logger(self._log, attribute)
        else:
            return attribute

    def __str__(self):
        result = "".join(self._log)
        return result
    

class Child(Logger):
    def __init__(self):
        self.name = "Vasya"

    def do(self, smth):
        print(smth + self.name)
        return smth

    