import inspect

class AbstractMetaclass():
    # В этом классе создается
    @staticmethod
    def create(name, mro): # pragma: no cover
        globals().update({el.__name__: el for el in mro[0]})  # Обновляем/дополняем содержимое словаря globals
        if len(mro[0]) != 0:
            bases = ",".join([base.__name__ for base in mro[0]])  # Если длина больше нуля то создаем переменную bases, начиная с запятой, в которую загружаем данные из mro
        else:
            bases = "" # в противном случае инициализируем пустую строковую переменную
        exec(f"class {name}({bases}):\n\tpass")  # запускаем через строку наши данные, переданные в функцию create
        # Создаем исполняемый класс
        metaclass = eval(f"{name}")  
        return metaclass


class AbstractClass():
    @staticmethod
    def create(name, mro): # pragma: no cover
        globals().update({el.__name__: el for el in mro[0]})
        globals().update({mro[1].__name__: mro[1]})
        if len(mro[0]) != 0:
            bases = ",".join([base.__name__ for base in mro[0]])
        else:
            bases = ""
        if mro[1]:
            meta = "metaclass=" + mro[1].__name__
        else:
            meta = ""
        if bases != "":
            str_ = bases + ", " + meta
        else:
            str_ = meta
        exec(f"class {name}({str_}):\n\tpass")
        _class = eval(f"{name}")
        return _class


def create_classbase(name, mro=None):
    if mro[1]:  # Если существует второй родитель
        template = AbstractClass.create(name, mro)
    else:
        template = AbstractMetaclass.create(name, mro)
    return template


def set_classattrs(cls, attributes=None):  # устанавливаем аттрибуты класса
    if attributes:
        for el in attributes:
            if el[1] != None:
                try:
                    if el[2] == "static method":
                        setattr(cls, el[0], staticmethod(el[1]))
                    elif el[2] == "class method":
                        setattr(cls, el[0], classmethod(el[1]))
                    else: # pragma: no cover
                        setattr(cls, el[0], el[1])
                except AttributeError: # pragma: no cover
                    continue
    return cls


def create_class(name, mro=None, attributes=None): # pragma: no cover
    if mro[1]:
        template = AbstractClass.create(name, mro)
    else:
        template = AbstractMetaclass.create(name, mro)
    if attributes:
        for el in attributes:
            if el[0] == "__dict__" or el[0] == "__weakref__": # weakref - ссылка на словарь или кэш, кторый скоро удалица
                continue
            if el[1] != None:
                try:
                    if el[2] == "static method":
                        setattr(template, el[0], staticmethod(el[1]))
                    elif el[2] == "class method":
                        setattr(template, el[0], classmethod(el[1]))
                    else:
                        setattr(template, el[0], el[1])
                except AttributeError:
                    continue
    return template


def create_instance(type_, fields): # Создаем сущность в зависимости от типа и добавляем соотв. аттрибуты
    instance = type_.__new__(type_)
    for el in fields:
        setattr(instance, el, fields[el])
    return instance


def cell_factory(el): # pragma: no cover
    inner = el

    def _f(): # задаем функцию чтобы передавать замыкание для объектов функций, передает кортеж cellov
        return el

    return _f.__closure__[0]  # передаем первый cell


def get_code(obj):  # получаем пожилой код в массив и отправляем его обязательно с переноса для дальнейшего использования
    lines = inspect.getsourcelines(obj)[0]
    tabs = 0
    for ch in lines[0]:
        if ch == ' ':
            tabs += 1
        else:
            break
    new_lines = []
    for line in lines:
        if len(line) >= tabs:
            line = line[tabs:]
        else:
            pass
        new_lines.append(line)
    return "\n".join(new_lines)