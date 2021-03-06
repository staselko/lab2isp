import builtins
import inspect
import re

primitives = {int, float, bool, str}  # Сет из основных примитивных типов в питоне


# С помощью регулярок, узнаем, есть ли в строке магическое выражение
def is_magicmarked(s: str) -> bool:  
    return re.match("^__(?:\w+)__$", s) != None


 # Является ли этот объект примитивом
def is_primitive(obj: object) -> bool: 
    return type(obj) in primitives

# Является ли объект названием класа функции или лист кортеж сет словарь

def is_basetype(obj: object) -> bool: 
    for el in primitives:
        if el.__name__ == obj.__name__:
            return True
    if el in [dict, list, tuple, set]:
        if el.__name__ == obj.__name__:
            return True
    return False


def is_instance(obj):  # pragma: no cover
    if not hasattr(obj, '__dict__'):
        return False
    if inspect.isroutine(obj): # ЯВЛЯЕТСЯ ЛИ ЭТОТ ОБЪЕКТ ФУНКЦИЕЙ ИЛИ МЕТОДОМ
        return False
    if inspect.isclass(obj): # КЛАССОМ
        return False
    else:
        return True


def is_none(obj: object) -> bool:
    return obj is None


def fetch_typereferences(cls): # Функция находит подителей и отношения между ними
    if inspect.isclass(cls):
        mro = inspect.getmro(cls)
        metamro = inspect.getmro(type(cls)) # получаем родителей у типа этого объекта
        metamro = tuple(cls for cls in metamro if cls not in (type, object)) # получаем все метаклассы этого класа
        class_bases = mro
        if not type in mro and len(metamro) != 0:  # если в мро нет тайпа лупим все элементы класс бейзеса кроме первого и последнего потому что там ненужные штуки
            return class_bases[1:-1], metamro[0]
        else:  # pragma: no cover
            return class_bases[1:-1], None


def fetch_funcreferences(func: object):  # pragma: no cover #обзор функций сначала мы
    if inspect.ismethod(func): #проверяем является ли функция методом
        func = func.__func__

    if not inspect.isfunction(func):  # проверка от обратного: валидная ли функция эта вообще
        raise TypeError("{!r} is not a Python function".format(func))

    code = func.__code__  #берем код нашего метода
    if func.__closure__ is None:  # созаем пустой словарь если рез отрицательный 
        nonlocal_vars = {}
    else:     #если же это замыкание добавляем поля в наш словарь
        nonlocal_vars = {  
            var: cell.cell_contents
            for var, cell in zip(code.co_freevars, func.__closure__)
        }

    global_ns = func.__globals__
    builtin_ns = global_ns.get("__builtins__", builtins.__dict__)
    if inspect.ismodule(builtin_ns):      # проверка на то является ли функция модулем 
        builtin_ns = builtin_ns.__dict__
    global_vars = {}   # регаем поля для дальнейшей обработки
    builtin_vars = {}
    unbound_names = set()
    for name in code.co_names:  # здесь мы уже достаем код функции и записываем в выше перечисленные переменные
        if name in ("None", "True", "False"):
            continue
        try:
            global_vars[name] = global_ns[name]
        except KeyError:
            try:
                builtin_vars[name] = builtin_ns[name]
            except KeyError:
                unbound_names.add(name)

    return (nonlocal_vars, global_vars,
            builtin_vars, unbound_names)


#тут уже собственно идет забор? ну да забираем все поля и класса по примеру объекта и тд

def deconstruct_class(cls):  
    attributes = inspect.classify_class_attrs(cls)
    deconstructed = []
    for attr in attributes:
        if attr.defining_class == object or attr.defining_class == type or attr.name in ["__dict__",
                                                                                         "__weakref__"]:  
            continue
        else:
            deconstructed.append((
                attr.name,
                attr.object,
                attr.kind
            ))
    return deconstructed


def deconstruct_func(func):
    code = {el: getattr(func.__code__, el) for el in func.__code__.__dir__() if not is_magicmarked(el) and "co" in el}

    refs = fetch_funcreferences(func)
    defaults = func.__defaults__
    return {'.name': func.__name__, '.code': code, '.references': refs, '.defaults': defaults}


def getfields(obj):  # pragma: no cover
    """Try to get as much attributes as possible"""
    members = inspect.getmembers(obj)

    cls = type(obj)
    type_attrnames = [el.name for el in inspect.classify_class_attrs(cls)]

    result = {}

    for member in members:
        if not member[0] in type_attrnames:
            result[member[0]] = member[1]

    return result


def deconstruct_instance(obj):  # pragma: no cover
    type_ = type(obj)
    fields = getfields(obj)

    return (type_, fields)