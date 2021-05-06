import datetime

sample_int = 123445
sample_float = 0.42
sample_bool = True
sample_string = "abacaba"
sample_None = None
sample_datetime = datetime.datetime(2021, 4, 10)
sample_tuple = (1, 2, 3)
sample_list = ["12, ", None, False, sample_tuple]
sample_dict = {sample_int: sample_bool,
               sample_string: sample_tuple}
sample_set = set()
for i in [1, 12, sample_int, 2, sample_int, sample_string, 1]:
    sample_set.add(i)

sample_frozenset = frozenset(sample_string)


def sample_func(n):
    return sample_float * n


def sample_generator():
    val = 1
    for i in range(10):
        yield val
        val += 1


def sample_fibonacci(n):
    if n == 1 or n == 0:
        return 1
    else:
        return sample_fibonacci(n - 1) + sample_fibonacci(n - 2)


def sample_inner_func(n):
    def inner(x):
        return x ** x

    return inner(inner(n) + n)


sample_lambda = lambda x: x ** 3


class A:
    def __init__(self):
        self.x = 12


a = A()
a.q = 2


class B:
    @staticmethod
    def static():
        return "hello from static method"

    def non_static(self):
        return "hey from self method"


class C(A):
    def __init__(self, prop):
        A.__init__(self)
        self._prop = prop

    @property
    def prop(self):
        return self._prop

    @prop.setter
    def prop(self, value):
        self._prop = value


class UpperAttrMetaclass(type):

    def __new__(cls, clsname, bases, dct):

        uppercase_attr = {}
        for name, val in dct.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val

        return super(UpperAttrMetaclass, cls).__new__(cls, clsname, bases, uppercase_attr)


class Foo(metaclass=UpperAttrMetaclass):
    bar = 'bip'
