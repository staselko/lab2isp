class AbstractMetaclass():
    @staticmethod
    def create(name, mro): # pragma: no cover
        globals().update({el.__name__: el for el in mro[0]})
        if len(mro[0]) != 0:
            bases = ",".join([base.__name__ for base in mro[0]])
        else:
            bases = ""
        exec(f"class {name}({bases}):\n\tpass")
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
    if mro[1]:
        template = AbstractClass.create(name, mro)
    else:
        template = AbstractMetaclass.create(name, mro)
    return template


def set_classattrs(cls, attributes=None): # pragma: no cover
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
            if el[0] == "__dict__" or el[0] == "__weakref__":
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


def create_instance(type_, fields): # pragma: no cover
    instance = type_.__new__(type_)
    for el in fields:
        setattr(instance, el, fields[el])
    return instance


def cell_factory(el): # pragma: no cover
    inner = el

    def _f():
        return el

    return _f.__closure__[0]


def get_code(obj): # pragma: no cover
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
