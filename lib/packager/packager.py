import builtins # pragma: no cover
import os # pragma: no cover

from datetime import datetime # pragma: no cover
import inspect # pragma: no cover
from types import FunctionType, CodeType
from sys import builtin_module_names, modules
from lib.packager.objectinspector import * # pragma: no cover
from lib.packager.creator import * # pragma: no cover


class Packer:
    def pack(self, obj: object):
        self.metainfo = {}
        self.proceeded = []
        dump = self.dump(obj)
        if len(self.metainfo) == 0: # Если нету данных в словаре, то вызываем функцию dump
            return dump
        else:
            return {".META": self.metainfo, ".OBJ": dump}  # В другом случае, возвращаем словарь двумя ключами

    def funcdump(self, obj, isstatic=False):
        obj_id = id(obj) # Получаем идентификатор объекта

        if isinstance(obj, staticmethod): # Если объект является статическим методом, то мы возвращаем функцию, которая будет работать с объектом функции
            return self.funcdump(obj.__func__, True)

        function_module = getattr(obj, "__module__", None)

        if function_module != None and function_module in builtin_module_names:  # Если function module имеет в себе аттрибуты и существует в зарезервированных именах, то суём в метаинфо содержимое

            self.metainfo.update({str(obj_id): {".metatype": "builtin func",
                                                ".name": obj.__name__,
                                                ".module": obj.__module__}})
        else: # В любом другом случае вызываем метод деконстракт функ

            dumped = deconstruct_func(obj) # Разбираем функцию на аттрибуты

            code_dict = dumped[".code"] # Получаем словарь из кода по ключу код и все, что с ним связано, упорядочиваем по ключам
            code_dict["co_code"] = [el for el in code_dict["co_code"]]
            code_dict["co_lnotab"] = [el for el in code_dict["co_lnotab"]]

            if self.metainfo.get(str(obj_id)) == None: # Если у объекта не оказалось айди, то просто суем все что нашли в метаинфо
                self.metainfo.update({str(obj_id): {".code": self.dump(code_dict),
                                                    ".metatype": "func",
                                                    ".name": self.dump(dumped[".name"]),
                                                    ".module": getattr(obj, "__module__", None),
                                                    ".refs": self.dump(dumped[".references"]),
                                                    ".defaults": self.dump(dumped[".defaults"])}})

            return {".metaid": str(obj_id)}  # возвращаем айди

    def dump(self, obj: object):  # Данная функция упаковывает наш объект и возвращает словарь со всеми данными
        obj_id = id(obj)

        if is_none(obj):
            return None

        if is_primitive(obj):
            return obj

        if type(obj) in [list, set, tuple, dict, frozenset]:
            if isinstance(obj, dict):
                result = {key: self.dump(obj[key]) for key in obj}  # Если является словарем, то раскидываем словарь через дамп каждый элемент будет примитивом
            elif type(obj) in [frozenset, set, tuple]:
                result = {".list": [self.dump(el) for el in obj], ".collection_type": f"{obj.__class__.__name__}"} # раскидываем в словарь с ключом .list тк массив
            else:
                result = [self.dump(el) for el in obj]
            return result

        if isinstance(obj, datetime):
            return {".time": str(obj.isoformat())}

        if obj_id in self.proceeded:  # Если айди есть в массиве то возвращаем этот айдишник
            return {".metaid": str(obj_id)}
        elif not getattr(obj, "__name__", None) in dir(builtins): # Если нет, то собственно добавляем, для работы с рекурсией
            self.proceeded.append(obj_id)

        if inspect.ismodule(obj): # Если у нашей функции есть модуль, которая она использует типа библиотеки, то смотрим и раскидываем его
            try: # В любом случае нужно добавить данные, которые мы получили
                if self.metainfo.get(str(obj_id)) == None:  # Если у нас нет аттрибутов у объекта то заносим их
                    if obj.__name__ in builtin_module_names:
                        self.metainfo.update({str(obj_id): {".metatype": "module", ".name": obj.__name__}})
                    else: # Если есть то закидываем еще и код, который мы получаем в функции гет код
                        self.metainfo.update(
                            {str(obj_id): {".code": get_code(obj), ".metatype": "module", ".name": obj.__name__}})
            except Exception:  # При любой возникшей ошибке, добавляем в словарь данные
                self.metainfo.update({str(obj_id): {".metatype": "module", ".name": obj.__name__}})
            return {".metaid": str(obj_id)} # Возвращем айдишник

        if getattr(obj, "__name__", None) and not is_basetype(obj): # Если объект не является базовым типом то ищем в списке буилтинов наше имя
            if obj.__name__ in dir(builtins): # Если оно есть то мы удаляем айдишник, тк они принадлежат библиотеке и перестаем работать с объектом через айди
                try:
                    self.proceeded.remove(str(obj_id))
                except Exception:
                    pass
                return {".metatype": "builtin", ".builtin": obj.__name__} # с этого момента у этого объекта не будет айди а будет метатип буилтин

            if inspect.ismethod(obj) or inspect.isfunction(obj) or isinstance(obj, staticmethod): # Если это функция какого либо рода то раскидываем через функдамп
                return self.funcdump(obj)

            if inspect.isbuiltin(obj): # Если этот айдишник является функцией built-in, то для нее есть свои данные метатипа, и с ней можно работать через айди
                self.metainfo.update(
                    {str(obj_id): {".metatype": "builtin-func", ".module": obj.__module__, ".name": obj.__name__}})
                return {".metaid": str(obj_id)}

            if is_instance(obj): # Если объект является сущностью, тоесть имеет свой dict то раскидываем его
                type_, fields = deconstruct_instance(obj) # Получаем тип и поля нашей сущности, получаем столько аттрибутов, сколько возможно
                type_id = id(type_)  # Получаем айдишник типа и потом начинаем раскидывать его, чтобы получилась полная картина
                self.dump(type_)

                data = {key: self.dump(fields[key]) for key in fields} # Раскидываем все поля через дамп и заносим их в словарь, чтобы получить все правильно для дальнейшей запаковки
                return {".metaid": str(type_id), ".fields": data} #Возвращаем айди и поля нашей сущности уже деконструированной

            if inspect.isclass(obj):  # Если класс

                mro = fetch_typereferences(obj) # Получаем данные о родителях, метаклассах
                attrs = deconstruct_class(obj) # Раскидываем класс по аттрибутам
                mro = [self.dump(el) for el in mro] # Еще раз делаем дамп, чтобы упорядочить наши поля в словаре
                attrs = [self.dump((el[0], self.dump(el[1]), el[2])) for el in attrs]  # То же самое

                if self.metainfo.get(str(obj_id)) == None: # Заканчиваем, упорядочиваем все, раскладываем по полочкам и получаем наш продукт
                    self.metainfo.update({str(obj_id): {".metatype": "class", ".name": obj.__name__,
                                                        ".module": getattr(obj, "__module__", None),
                                                        ".class": {"mro": mro, "attrs": attrs}}})

                return {".metaid": str(obj_id)} # Возвращем айди
        else: # Если же это базовый тип то все проще
            if inspect.ismethod(obj) or inspect.isfunction(obj) or isinstance(obj, staticmethod):  # Функцию раскидываем функдампом
                return self.funcdump(obj)

            if is_instance(obj):  # Сущность раскидываем как раскидывали выше
                type_, fields = deconstruct_instance(obj)
                type_id = id(type_)
                self.dump(type_)

                data = {key: self.dump(fields[key]) for key in fields}
                return {".metaid": str(type_id), ".fields": data}

            return None # pragma: no cover


class Unpacker:  # Теперь разархивируем
    def unpack(self, src: object, __globals__=globals()):
        self._globals = __globals__ # Получаем глобальные переменные для данного окружения
        if isinstance(src, dict): # Если сущность является словарем
            if src.get(".META") != None and src.get(".OBJ") != None: # Если у набора есть мета и обж то закидываем мета в локальную метадикт, создаем переменные для типов и айди
                self.metatypes = {}  # Метатипы это словарь, который содержит в себе все что нужно знать о нашем объекте
                self.proceeded = []
                self.metadict = src[".META"]
                return self.load(src[".OBJ"])
            else:
                return self.load(src)

        if is_none(src):
            return None

        if is_primitive(src): # Если примитив, просто возвращаем то,что получили на входе
            return src

        if isinstance(src, list): # Если массив, то раскидывваем через лоад по итерации
            return [self.load(el) for el in src]

    def load(self, src, id_=None): # Работаем здесь, упорядочиваем входные данные
        if is_none(src):
            return None

        if is_primitive(src):
            return src

        elif isinstance(src, list):  # Рекурсивно раскидываем каждый элемент
            return [self.load(el) for el in src]


        elif isinstance(src, dict):  # Если словарь
            if src.get(".metaid") != None and src.get(".metatype") == None: # Получаем metaid, у которого не должно быть metatype ключа
                meta_id = src[".metaid"]
                obj = None

                if src[".metaid"] in self.proceeded:  # Если есть метаid то по айди находим метатип
                    obj = self.metatypes[meta_id]
                else:
                    obj = self.load(self.metadict[meta_id], meta_id)  # Опять рекурсивно работаем с каждым элементом словаря metadict
                    self.metatypes[meta_id] = obj  # В метатип заносим наш объект
                    self.proceeded.append(meta_id)  # И айдишник заносим в preceeded
                if src.get(".fields"):  # Если есть поля входных данных
                    obj = create_instance(obj, self.load(src[".fields"]))  # Создаем сущность с ее аттрибутами
                return obj

            elif src.get(".metatype"):  # Если у входных данных есть .metatype
                metatype = src[".metatype"]  # Присваиваем перемнной метатайп значение нашего элемента в словаре

                if metatype == "func":  # если функция, то работаем как с функцией
                    if src[".module"] != "__main__":  # Если функция вызвана не из мейна то импортируем ее
                        try:
                            exec(f'from {src[".module"]} import {src[".name"]}')
                            return eval(f'{src[".name"]}')
                        except Exception:
                            pass

                    refs = self.load(src[".refs"])  # получаем опять рекурсивно refs
                    nonlocals = refs[0] # Получаем нелокальные переменные
                    globals_ = refs[1] # Глобальные

                    co_raw = self.load(src[".code"])  #Получаем словарь с кодом

                    co = CodeType(  # Раскидываем словарь с кодом в объект кода
                        co_raw["co_argcount"],
                        co_raw["co_posonlyargcount"],
                        co_raw["co_kwonlyargcount"],
                        co_raw["co_nlocals"],
                        co_raw["co_stacksize"],
                        co_raw["co_flags"],
                        bytes(co_raw["co_code"]),
                        co_raw["co_consts"],
                        co_raw["co_names"],
                        co_raw["co_varnames"],
                        co_raw["co_filename"],
                        co_raw["co_name"],
                        co_raw["co_firstlineno"],
                        bytes(co_raw["co_lnotab"]),
                        co_raw["co_freevars"],
                        co_raw["co_cellvars"]
                    )

                    for el in globals_:
                        if el in globals().keys():
                            continue
                        else:
                            globals()[el] = self.load(globals_[el])

                    closures = tuple(cell_factory(nonlocals[el]) for el in co.co_freevars)  # Получаем замыкающие ячейки

                    naked = [  # Получаем голый объект
                        co,
                        globals(),
                        src[".name"],
                        src[".defaults"],

                        closures
                    ]

                    func = FunctionType(*naked)   # Собираем функцию нашу воедино со всеми ее вытекающими аттрибутами
                    return func

                if metatype == "builtin-func": # Если встроенная функция опять через модуль ее импортируем
                    try:
                        exec(f'from {src[".module"]} import {src[".name"]}')
                        return eval(f'{src[".name"]}')
                    except Exception:
                        raise KeyError(f'builtin func "{src[".module"]}.{src[".name"]}" import failed')  # Если допустим не установлен модуль

                elif metatype == "class":  # Если класс то смотрим на то откуда вызываем
                    if src[".module"] != "__main__":
                        try:
                            exec(f'from {src[".module"]} import {src[".name"]}')
                            return eval(f'{src[".name"]}')
                        except Exception:
                            pass

                    class_info = src[".class"]  # Информация о классе
                    mro = self.load(class_info["mro"]) # Родителях
                    cls = create_classbase(src[".name"], mro) # Создаем наш класс по аттрибутам и родитлям

                    self.metatypes[id_] = cls
                    self.proceeded.append(id_)

                    attrs = self.load(class_info["attrs"]) # Аттрибуты закинули и вернули

                    return set_classattrs(cls, attrs)

                elif metatype == "module": # Если это модуль который мы импортируем
                    try:
                        exec(f'import {src[".name"]}')
                        result = eval(src[".name"])
                        return result
                    except Exception:
                        if ".code" in src.keys():  # не знаю тут что то по ключам оно делает все собирает в строчку и выполняет
                            with open("{}/{}.py".format("/".join(modules["__main__"].__file__.split('/')[:-1]),
                                                        src[".name"]), "w") as writer:
                                writer.write(src[".code"])
                            exec(f'import {src[".name"]}')
                            result = eval(src[".name"])
                            os.unlink(
                                "{}/{}.py".format("/".join(modules["__main__"].__file__.split('/')[:-1]), src[".name"]))
                            return result
                    raise KeyError(f'module"{src[".module"]}" import failed')

                elif metatype == "builtin": # Если это встроенная переменная то ее просто импортируем
                    if src.get(".builtin"):
                        return getattr(builtins, src[".builtin"])
                    else:
                        raise KeyError(f'builtin "{src[".builtin"]}" import failed')

                else:
                    raise KeyError(f"Unexpected metatype: {metatype}")

            elif src.get(".collection_type"):  # Если массив
                if src[".collection_type"] == "tuple":
                    return tuple(el for el in self.load(src[".list"]))
                elif src[".collection_type"] == "set":
                    return set(el for el in self.load(src[".list"]))
                elif src[".collection_type"] == "frozenset":
                    return frozenset(el for el in self.load(src[".list"]))
                else:
                    return self.load(src[".list"])

            elif src.get(".time"):
                date = datetime.fromisoformat(src[".time"])
                return date

            else:
                res = {
                    key: self.load(src[key]) for key in src
                }

                return res # это если прям совсем ничто
