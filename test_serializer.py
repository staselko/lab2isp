from lib import Serializer
from tests.sample_objects import *
import math

ser = Serializer.Serializer()
ser.change_form('toml')


class TestPrimesJson:
    def test_tuple(self):
        ser.string = '{".list": [1, 2, 3], ".collection_type": "tuple"}'
        
        assert ser.loads(ser.string) == sample_tuple

    def test_int(self):
        ser.string = '123445'
        
        assert ser.loads(ser.string) == sample_int

    def test_float(self):
        ser.string = '0.42'
        assert math.isclose(ser.loads(ser.string), sample_float)

    def test_bool(self):
        ser.string = 'true'
        assert ser.loads(ser.string) == sample_bool

    def test_string(self):
        ser.string = '"abacaba"'
        assert ser.loads(ser.string) == sample_string

    def test_datetime(self):
        ser.string = '{".time": "2021-04-10T00:00:00"}'
        assert ser.loads(ser.string) == sample_datetime

    def test_None(self):
        ser.string = 'null'
        assert ser.loads(ser.string) == sample_None

    def test_dict(self):
        ser.string = '{"123445": true, "abacaba": {".list": [1, 2, 3], ".collection_type": "tuple"}}'
        assert isinstance(ser.loads(ser.string), dict)
        assert ser.loads(ser.string)["123445"] == sample_bool
        assert ser.loads(ser.string)[sample_string] == sample_tuple

    def test_list(self):
        ser.string = '["12, ", null, false, {".list": [1, 2, 3], ".collection_type": "tuple"}]'
        assert ser.loads(ser.string) == sample_list

    def test_set(self):
        ser.string = '{".list": [1, 2, "abacaba", 12, 123445], ".collection_type": "set"}'
        assert isinstance(ser.loads(ser.string), set)
        assert len(ser.loads(ser.string)) == 5
        for i in sample_set:
            assert i in ser.loads(ser.string)

    def test_frozenset(self):
        ser.string = '{".list": ["c", "a", "b"], ".collection_type": "frozenset"}'
        assert isinstance(ser.loads(ser.string), frozenset)
        assert len(ser.loads(ser.string)) == 3
        data = ser.loads(ser.string)
        for i in sample_frozenset:
            assert i in data


class TestFunctionsJson:
    def test_func(self):
        ser.string = '{".META": {"139665363508960": {".code": {"co_argcount": 1, "co_posonlyargcount": 0, "co_kwonlyargcount": 0, "co_nlocals": 1, "co_stacksize": 2, "co_flags": 67, "co_code": [116, 0, 124, 0, 20, 0, 83, 0], "co_consts": {".list": [null], ".collection_type": "tuple"}, "co_names": {".list": ["sample_float"], ".collection_type": "tuple"}, "co_varnames": {".list": ["n"], ".collection_type": "tuple"}, "co_freevars": {".list": [], ".collection_type": "tuple"}, "co_cellvars": {".list": [], ".collection_type": "tuple"}, "co_filename": "/home/slava/Public/Testing/tests/sample_objects.py", "co_name": "sample_func", "co_firstlineno": 20, "co_lnotab": [0, 1]}, ".metatype": "func", ".name": "sample_func", ".module": "tests.sample_objects", ".refs": {".list": [{}, {"sample_float": 0.42}, {}, {".list": [], ".collection_type": "set"}], ".collection_type": "tuple"}, ".defaults": null}}, ".OBJ": {".metaid": "139665363508960"}}'
        assert math.isclose(ser.loads(ser.string)(2.4), 1.008)

    def test_generator(self):
        ser.string = '{".META": {"140418400387136": {".code": {"co_argcount": 0, "co_posonlyargcount": 0, "co_kwonlyargcount": 0, "co_nlocals": 2, "co_stacksize": 3, "co_flags": 99, "co_code": [100, 1, 125, 0, 116, 0, 100, 2, 131, 1, 68, 0, 93, 18, 125, 1, 124, 0, 86, 0, 1, 0, 124, 0, 100, 1, 55, 0, 125, 0, 113, 12, 100, 0, 83, 0], "co_consts": {".list": [null, 1, 10], ".collection_type": "tuple"}, "co_names": {".list": ["range"], ".collection_type": "tuple"}, "co_varnames": {".list": ["val", "i"], ".collection_type": "tuple"}, "co_freevars": {".list": [], ".collection_type": "tuple"}, "co_cellvars": {".list": [], ".collection_type": "tuple"}, "co_filename": "/home/slava/Public/Testing/tests/sample_objects.py", "co_name": "sample_generator", "co_firstlineno": 24, "co_lnotab": [0, 1, 4, 1, 12, 1, 6, 1]}, ".metatype": "func", ".name": "sample_generator", ".module": "tests.sample_objects", ".refs": {".list": [{}, {}, {"range": {".metatype": "builtin", ".builtin": "range"}}, {".list": [], ".collection_type": "set"}], ".collection_type": "tuple"}, ".defaults": null}}, ".OBJ": {".metaid": "140418400387136"}}'
        data = [val for val in ser.loads(ser.string)()]
        assert data == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_fibonacci(self):
        ser.string = '{".META": {"140292067798896": {".code": {"co_argcount": 1, "co_posonlyargcount": 0, "co_kwonlyargcount": 0, "co_nlocals": 1, "co_stacksize": 4, "co_flags": 67, "co_code": [124, 0, 100, 1, 107, 2, 115, 16, 124, 0, 100, 2, 107, 2, 114, 20, 100, 1, 83, 0, 116, 0, 124, 0, 100, 1, 24, 0, 131, 1, 116, 0, 124, 0, 100, 3, 24, 0, 131, 1, 23, 0, 83, 0, 100, 0, 83, 0], "co_consts": {".list": [null, 1, 0, 2], ".collection_type": "tuple"}, "co_names": {".list": ["sample_fibonacci"], ".collection_type": "tuple"}, "co_varnames": {".list": ["n"], ".collection_type": "tuple"}, "co_freevars": {".list": [], ".collection_type": "tuple"}, "co_cellvars": {".list": [], ".collection_type": "tuple"}, "co_filename": "/home/slava/Public/Testing/tests/sample_objects.py", "co_name": "sample_fibonacci", "co_firstlineno": 24, "co_lnotab": [0, 1, 16, 1, 4, 2]}, ".metatype": "func", ".name": "sample_fibonacci", ".module": "tests.sample_objects", ".refs": {".list": [{}, {"sample_fibonacci": {".metaid": "140292067798896"}}, {}, {".list": [], ".collection_type": "set"}], ".collection_type": "tuple"}, ".defaults": null}}, ".OBJ": {".metaid": "140292067798896"}}'
        assert ser.loads(ser.string)(7) == 21

    def test_lambda(self):
        ser.string = '{".META": {"140224654409936": {".code": {"co_argcount": 1, "co_posonlyargcount": 0, "co_kwonlyargcount": 0, "co_nlocals": 1, "co_stacksize": 2, "co_flags": 67, "co_code": [124, 0, 100, 1, 19, 0, 83, 0], "co_consts": {".list": [null, 3], ".collection_type": "tuple"}, "co_names": {".list": [], ".collection_type": "tuple"}, "co_varnames": {".list": ["x"], ".collection_type": "tuple"}, "co_freevars": {".list": [], ".collection_type": "tuple"}, "co_cellvars": {".list": [], ".collection_type": "tuple"}, "co_filename": "/home/slava/Public/Testing/sample_objects.py", "co_name": "<lambda>", "co_firstlineno": 40, "co_lnotab": []}, ".metatype": "func", ".name": "<lambda>", ".module": "sample_objects", ".refs": {".list": [{}, {}, {}, {".list": [], ".collection_type": "set"}], ".collection_type": "tuple"}, ".defaults": null}}, ".OBJ": {".metaid": "140224654409936"}}'
        
        assert math.isclose(ser.loads(ser.string)(1.6), 4.096)

    def test_inner_func(self):
        ser.string = '{".META": {"140335234293824": {".code": {"co_argcount": 1, "co_posonlyargcount": 0, "co_kwonlyargcount": 0, "co_nlocals": 2, "co_stacksize": 3, "co_flags": 67, "co_code": [100, 1, 100, 2, 132, 0, 125, 1, 124, 1, 124, 1, 124, 0, 131, 1, 124, 0, 23, 0, 131, 1, 83, 0], "co_consts": {".list": [null, null, "sample_inner_func.<locals>.inner"], ".collection_type": "tuple"}, "co_names": {".list": [], ".collection_type": "tuple"}, "co_varnames": {".list": ["n", "inner"], ".collection_type": "tuple"}, "co_freevars": {".list": [], ".collection_type": "tuple"}, "co_cellvars": {".list": [], ".collection_type": "tuple"}, "co_filename": "/home/slava/Public/Testing/tests/sample_objects.py", "co_name": "sample_inner_func", "co_firstlineno": 31, "co_lnotab": [0, 1, 8, 3]}, ".metatype": "func", ".name": "sample_inner_func", ".module": "tests.sample_objects", ".refs": {".list": [{}, {}, {}, {".list": [], ".collection_type": "set"}], ".collection_type": "tuple"}, ".defaults": null}}, ".OBJ": {".metaid": "140335234293824"}}'
        
        assert math.isclose(ser.loads(ser.string)(1.99), 37643.98251178124)


class TestClassesJson:
    def test_class_A(self):
        a = ser.load('tests/classA.json')
        instance = a()
        assert a.__name__ == 'A'
        assert type(a) == type
        assert instance.x == 12

    def test_class_B(self):
        a = ser.load('tests/classB.json')
        instance = a()
        assert a.__name__ == 'B'
        assert type(a) == type
        assert instance.non_static() == "hey from self method"
        assert a.static() == "hello from static method"

    def test_class_C(self):
        a = ser.load('tests/classC.json')
        instance = a(lambda x: x + x)
        assert a.__name__ == 'C'
        assert a.__base__.__name__ == 'A'
        assert type(a) == type
        assert instance.x == 12
        assert instance.prop("42") == "4242"

    def test_class_Foo(self):
        a = ser.load('tests/classFoo.json')
        assert not hasattr(a, 'bar')
        assert hasattr(a, 'BAR')
        f = a()
        assert f.BAR == "bip"


class TestPackUnpackJson:
    def test_tuple(self):
        a = sample_tuple
        assert ser.loads(ser.dumps(a)) == sample_tuple

    def test_int(self):
        a = sample_int
        assert ser.loads(ser.dumps(a)) == sample_int

    def test_float(self):
        a = sample_float
        assert math.isclose(ser.loads(ser.dumps(a)), sample_float)

    def test_bool(self):
        a = sample_bool
        assert ser.loads(ser.dumps(a)) == sample_bool

    def test_string(self):
        a = sample_string
        assert ser.loads(ser.dumps(a)) == sample_string

    def test_datetime(self):
        a = sample_datetime
        assert ser.loads(ser.dumps(a)) == sample_datetime

    def test_None(self):
        a = sample_None
        assert ser.loads(ser.dumps(a)) == sample_None

    def test_dict(self):
        a = sample_dict
        d = ser.loads(ser.dumps(a))
        assert isinstance(d, dict)
        assert d[123445] == sample_bool
        assert d[sample_string] == sample_tuple

    def test_list(self):
        a = sample_list
        assert ser.loads(ser.dumps(a)) == sample_list

    def test_set(self):
        a = sample_set
        assert isinstance(ser.loads(ser.dumps(a)), set)
        assert len(ser.loads(ser.dumps(a))) == 5
        for i in sample_set:
            assert i in ser.loads(ser.dumps(a))

    def test_frozenset(self):
        a = sample_frozenset
        assert isinstance(ser.loads(ser.dumps(a)), frozenset)
        assert len(ser.loads(ser.dumps(a))) == 3
        for i in sample_frozenset:
            assert i in ser.loads(ser.dumps(a))

    def test_func(self):
        a = sample_func
        assert math.isclose(ser.loads(ser.dumps(a))(2.4), 1.008)

    def test_funcname(self):

        def func():
            return "works"

        a = func
        assert ser.loads(ser.dumps(a))() == "works"

    def test_generator(self):
        a = sample_generator
        
        data = [val for val in ser.loads(ser.dumps(a))()]
        assert data == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_fibonacci(self):
        a = sample_fibonacci
        
        assert ser.loads(ser.dumps(a))(7) == 21

    def test_lambda(self):
        a = sample_lambda
        
        assert math.isclose(ser.loads(ser.dumps(a))(1.6), 4.096)

    def test_inner_func(self):
        a = sample_inner_func
        
        assert math.isclose(ser.loads(ser.dumps(a))(1.99), 37643.98251178124)

    def test_class_A(self):
        a = A
        
        instance = ser.loads(ser.dumps(a))()
        assert ser.loads(ser.dumps(a)).__name__ == 'A'
        assert type(ser.loads(ser.dumps(a))) == type
        assert instance.x == 12

    def test_class_B(self):
        a = B
        
        instance = ser.loads(ser.dumps(a))()
        assert ser.loads(ser.dumps(a)).__name__ == 'B'
        assert type(ser.loads(ser.dumps(a))) == type
        assert instance.non_static() == "hey from self method"
        assert ser.loads(ser.dumps(a)).static() == "hello from static method"

    def test_class_C(self):
        a = C
        
        instance = ser.loads(ser.dumps(a))(lambda x: x + x)
        assert ser.loads(ser.dumps(a)).__name__ == 'C'
        assert ser.loads(ser.dumps(a)).__base__.__name__ == 'A'
        assert type(ser.loads(ser.dumps(a))) == type
        assert instance.x == 12
        assert instance.prop("42") == "4242"

    def test_class_Foo(self):
        a = Foo
        
        assert not hasattr(ser.loads(ser.dumps(a)), 'bar')
        assert hasattr(ser.loads(ser.dumps(a)), 'BAR')
        f = ser.loads(ser.dumps(a))()
        assert f.BAR == "bip"


ser.change_form('yaml')


class TestClassesJson:
    def test_class_A(self):
        a = ser.load('tests/classA.json')
        instance = a()
        assert ser.loads(ser.dumps(a)).__name__ == 'A'
        assert type(ser.loads(ser.dumps(a))) == type
        assert instance.x == 12

    def test_class_B(self):
        a = ser.load('tests/classB.json')
        instance = ser.loads(ser.dumps(a))()
        assert ser.loads(ser.dumps(a)).__name__ == 'B'
        assert type(ser.loads(ser.dumps(a))) == type
        assert instance.non_static() == "hey from self method"
        assert ser.loads(ser.dumps(a)).static() == "hello from static method"

    def test_class_C(self):
        a = ser.load('tests/classC.json')
        instance = ser.loads(ser.dumps(a))(lambda x: x + x)
        assert ser.loads(ser.dumps(a)).__name__ == 'C'
        assert ser.loads(ser.dumps(a)).__base__.__name__ == 'A'
        assert type(ser.loads(ser.dumps(a))) == type
        assert instance.x == 12
        assert instance.prop("42") == "4242"

    def test_class_Foo(self):
        a = ser.load('tests/classFoo.json')
        assert not hasattr(ser.loads(ser.dumps(a)), 'bar')
        assert hasattr(ser.loads(ser.dumps(a)), 'BAR')
        f = ser.loads(ser.dumps(a))()
        assert f.BAR == "bip"


class TestPackUnpackYaml:
    def test_tuple(self):
        a = sample_tuple
        
        assert ser.loads(ser.dumps(a)) == sample_tuple

    def test_int(self):
        a = sample_int
        
        assert ser.loads(ser.dumps(a)) == sample_int

    def test_float(self):
        a = sample_float
        
        assert math.isclose(ser.loads(ser.dumps(a)), sample_float)

    def test_bool(self):
        a = sample_bool
        
        assert ser.loads(ser.dumps(a)) == sample_bool

    def test_string(self):
        a = sample_string
        
        assert ser.loads(ser.dumps(a)) == sample_string

    def test_datetime(self):
        a = sample_datetime
        
        assert ser.loads(ser.dumps(a)) == sample_datetime

    def test_None(self):
        a = sample_None
        
        assert ser.loads(ser.dumps(a)) == sample_None

    def test_dict(self):
        a = sample_dict
        
        assert isinstance(ser.loads(ser.dumps(a)), dict)
        assert ser.loads(ser.dumps(a))[123445] == sample_bool
        assert ser.loads(ser.dumps(a))[sample_string] == sample_tuple

    def test_list(self):
        a = sample_list
        
        assert ser.loads(ser.dumps(a)) == sample_list

    def test_set(self):
        a = sample_set
        
        assert isinstance(ser.loads(ser.dumps(a)), set)
        assert len(ser.loads(ser.dumps(a))) == 5
        for i in sample_set:
            assert i in ser.loads(ser.dumps(a))

    def test_frozenset(self):
        a = sample_frozenset
        
        assert isinstance(ser.loads(ser.dumps(a)), frozenset)
        assert len(ser.loads(ser.dumps(a))) == 3
        for i in sample_frozenset:
            assert i in ser.loads(ser.dumps(a))

    def test_func(self):
        a = sample_func
        
        assert math.isclose(ser.loads(ser.dumps(a))(2.4), 1.008)

    def test_funcname(self):

        def func():
            return "works"

        a = func
        
        assert ser.loads(ser.dumps(a))() == "works"

    def test_generator(self):
        a = sample_generator
        
        data = [val for val in ser.loads(ser.dumps(a))()]
        assert data == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_fibonacci(self):
        a = sample_fibonacci
        
        assert ser.loads(ser.dumps(a))(7) == 21

    def test_lambda(self):
        a = sample_lambda
        
        assert math.isclose(ser.loads(ser.dumps(a))(1.6), 4.096)

    def test_inner_func(self):
        a = sample_inner_func
        
        assert math.isclose(ser.loads(ser.dumps(a))(1.99), 37643.98251178124)

    def test_class_A(self):
        a = A
        
        instance = ser.loads(ser.dumps(a))()
        assert ser.loads(ser.dumps(a)).__name__ == 'A'
        assert type(ser.loads(ser.dumps(a))) == type
        assert instance.x == 12

    def test_class_B(self):
        a = B
        
        instance = ser.loads(ser.dumps(a))()
        assert ser.loads(ser.dumps(a)).__name__ == 'B'
        assert type(ser.loads(ser.dumps(a))) == type
        assert instance.non_static() == "hey from self method"
        assert ser.loads(ser.dumps(a)).static() == "hello from static method"

    def test_class_C(self):
        a = C
        
        instance = ser.loads(ser.dumps(a))(lambda x: x + x)
        assert ser.loads(ser.dumps(a)).__name__ == 'C'
        assert ser.loads(ser.dumps(a)).__base__.__name__ == 'A'
        assert type(ser.loads(ser.dumps(a))) == type
        assert instance.x == 12
        assert instance.prop("42") == "4242"

    def test_class_Foo(self):
        a = Foo
        
        assert not hasattr(ser.loads(ser.dumps(a)), 'bar')
        assert hasattr(ser.loads(ser.dumps(a)), 'BAR')
        f = ser.loads(ser.dumps(a))()
        assert f.BAR == "bip"


class TestClassesYaml:
    def test_class_A(self):
        a = ser.load('tests/classA.yaml')
        instance = ser.loads(ser.dumps(a))()
        assert ser.loads(ser.dumps(a)).__name__ == 'A'
        assert type(ser.loads(ser.dumps(a))) == type
        assert instance.x == 12

    def test_class_B(self):
        a = ser.load('tests/classB.yaml')
        instance = ser.loads(ser.dumps(a))()
        assert ser.loads(ser.dumps(a)).__name__ == 'B'
        assert type(ser.loads(ser.dumps(a))) == type
        assert instance.non_static() == "hey from self method"
        assert ser.loads(ser.dumps(a)).static() == "hello from static method"

    def test_class_C(self):
        a = ser.load('tests/classC.yaml')
        instance = ser.loads(ser.dumps(a))(lambda x: x + x)
        assert ser.loads(ser.dumps(a)).__name__ == 'C'
        assert ser.loads(ser.dumps(a)).__base__.__name__ == 'A'
        assert type(ser.loads(ser.dumps(a))) == type
        assert instance.x == 12
        assert instance.prop("42") == "4242"

    def test_class_Foo(self):
        a = ser.load('tests/classFoo.yaml')
        assert not hasattr(ser.loads(ser.dumps(a)), 'bar')
        assert hasattr(ser.loads(ser.dumps(a)), 'BAR')
        f = ser.loads(ser.dumps(a))()
        assert f.BAR == "bip"
