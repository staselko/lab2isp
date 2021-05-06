from abc import abstractmethod
import inspect
import functools

class ModelCreator(type):
    def __new__(cls, *args):
        field_dict = {}
        for base in args[1]:
            if getattr(base, "__fields__", None) != None:
                field_dict.update(base.__fields__)
        for attr in args[2]:
            if isinstance(args[2][attr], AbstractField):
                field_dict.update({attr: args[2][attr]})
        obj = super(ModelCreator, cls).__new__(cls, *args)
        setattr(obj, "__fields__", field_dict)
        obj.__setattr__ = ModelCreator._wrapped_setattr(obj.__setattr__)
        obj.__init__ = ModelCreator._wrapped_init(obj.__init__)
        return obj

    @staticmethod
    def _wrapped_init(default_init):
        def field_init(self, *args, **kwargs):
            init_params = inspect.signature(default_init).parameters
            for param in init_params:
                if init_params[param]._kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                    if self.__fields__.get(init_params[param]._name) != None:
                        raise SyntaxError(f"ModelCreator got conflict with {self.__class__}.__init__() args\nSolve conflict with attribute: '{param}'")
            for field in self.__fields__:
                if kwargs.get(field) != None:
                    self.__setattr__(field, kwargs[field])
                    kwargs.pop(field)
                else:
                    if getattr(self, field, None) == None or isinstance(getattr(self, field, None), AbstractField):
                        raise TypeError(f"{self.__class__}.__init__() missing required keyword-only argument: '{field}'")
            default_init(self, *args, **kwargs)
        return field_init
    
    @staticmethod
    def _wrapped_setattr(default_setattr):
        def setattr(self, name, value):
            if name in self.__fields__:
                default_setattr(self, name, self.__fields__[name].field_checker(value))
            else:
                default_setattr(self, name, value)
        return setattr

class AbstractField:
    def __init__(self, field_type: type):
        self._type = field_type

    def field_checker(self, val):
        if (isinstance(val, self._type)):
            return val
        else:
            raise TypeError(f"Expected attr type is {self._type.__name__} but got {type(val)}")


class Person(metaclass=ModelCreator):
    name = AbstractField(str)
    def __init__(self) -> None:
        pass

class Student(Person):
    average = AbstractField(float)
    inner_list = AbstractField(list)
    inner_dict = AbstractField(dict)
    def __init__(self) -> None:
        super().__init__()