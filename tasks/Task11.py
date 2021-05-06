class Singleton(type):
    def __new__(cls, *args):
        type_ = super(Singleton, cls).__new__(cls, *args)
        if args[2].get("__new__") != None:
            type_.__new__ = Singleton._new_wrapper(type_.__new__, False)
        else:
            type_.__new__ = Singleton._new_wrapper(type_.__new__, True)
        type_._instance = None
        return type_

    @staticmethod
    def _new_wrapper(func, is_implicit):
        def _subclass_new(cls, *args, **kwargs):
            if cls._instance == None:
                if is_implicit == True:
                    obj = func(cls)
                else:
                    obj = func(cls, *args, **kwargs)
                cls._instance = obj
            return cls._instance
        return _subclass_new
        

class Subclass(metaclass=Singleton):
    def __new__(cls, *args, **kwargs):
        obj = super(Subclass, cls).__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj
    
    def __init__(self, name):
        self.name = name
        
class Subclass2(metaclass=Singleton):
    def __init__(self, name):
        self.name = name
        