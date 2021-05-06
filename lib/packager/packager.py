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
        if len(self.metainfo) == 0:
            return dump
        else:
            return {".META": self.metainfo, ".OBJ": dump}

    def funcdump(self, obj, isstatic=False):
        obj_id = id(obj)

        if isinstance(obj, staticmethod):
            return self.funcdump(obj.__func__, True)

        function_module = getattr(obj, "__module__", None)

        if function_module != None and function_module in builtin_module_names:
            self.metainfo.update({str(obj_id): {".metatype": "builtin func",
                                                ".name": obj.__name__,
                                                ".module": obj.__module__}})
        else:

            dumped = deconstruct_func(obj)

            code_dict = dumped[".code"]
            code_dict["co_code"] = [el for el in code_dict["co_code"]]
            code_dict["co_lnotab"] = [el for el in code_dict["co_lnotab"]]

            if self.metainfo.get(str(obj_id)) == None:
                self.metainfo.update({str(obj_id): {".code": self.dump(code_dict),
                                                    ".metatype": "func",
                                                    ".name": self.dump(dumped[".name"]),
                                                    ".module": getattr(obj, "__module__", None),
                                                    ".refs": self.dump(dumped[".references"]),
                                                    ".defaults": self.dump(dumped[".defaults"])}})

            return {".metaid": str(obj_id)}

    def dump(self, obj: object):
        obj_id = id(obj)

        if is_none(obj):
            return None

        if is_primitive(obj):
            return obj

        if type(obj) in [list, set, tuple, dict, frozenset]:
            if isinstance(obj, dict):
                result = {key: self.dump(obj[key]) for key in obj}
            elif type(obj) in [frozenset, set, tuple]:
                result = {".list": [self.dump(el) for el in obj], ".collection_type": f"{obj.__class__.__name__}"}
            else:
                result = [self.dump(el) for el in obj]
            return result

        if isinstance(obj, datetime):
            return {".time": str(obj.isoformat())}

        if obj_id in self.proceeded:
            return {".metaid": str(obj_id)}
        elif not getattr(obj, "__name__", None) in dir(builtins):
            self.proceeded.append(obj_id)

        if inspect.ismodule(obj): # pragma: no cover
            try:
                if self.metainfo.get(str(obj_id)) == None:
                    if obj.__name__ in builtin_module_names:
                        self.metainfo.update({str(obj_id): {".metatype": "module", ".name": obj.__name__}})
                    else:
                        self.metainfo.update(
                            {str(obj_id): {".code": get_code(obj), ".metatype": "module", ".name": obj.__name__}})
            except Exception:
                self.metainfo.update({str(obj_id): {".metatype": "module", ".name": obj.__name__}})
            return {".metaid": str(obj_id)}

        if getattr(obj, "__name__", None) and not is_basetype(obj): # pragma: no cover
            if obj.__name__ in dir(builtins):
                try:
                    self.proceeded.remove(str(obj_id))
                except Exception:
                    pass
                return {".metatype": "builtin", ".builtin": obj.__name__}

            if inspect.ismethod(obj) or inspect.isfunction(obj) or isinstance(obj, staticmethod):
                return self.funcdump(obj)

            if inspect.isbuiltin(obj): 
                self.metainfo.update(
                    {str(obj_id): {".metatype": "builtin-func", ".module": obj.__module__, ".name": obj.__name__}})
                return {".metaid": str(obj_id)}

            if is_instance(obj): # pragma: no cover
                type_, fields = deconstruct_instance(obj)
                type_id = id(type_)
                self.dump(type_)

                data = {key: self.dump(fields[key]) for key in fields}
                return {".metaid": str(type_id), ".fields": data}

            if inspect.isclass(obj):

                mro = fetch_typereferences(obj)
                attrs = deconstruct_class(obj)
                mro = [self.dump(el) for el in mro]
                attrs = [self.dump((el[0], self.dump(el[1]), el[2])) for el in attrs]

                if self.metainfo.get(str(obj_id)) == None:
                    self.metainfo.update({str(obj_id): {".metatype": "class", ".name": obj.__name__,
                                                        ".module": getattr(obj, "__module__", None),
                                                        ".class": {"mro": mro, "attrs": attrs}}})

                return {".metaid": str(obj_id)}
        else:
            if inspect.ismethod(obj) or inspect.isfunction(obj) or isinstance(obj, staticmethod):
                return self.funcdump(obj)

            if is_instance(obj):
                type_, fields = deconstruct_instance(obj)
                type_id = id(type_)
                self.dump(type_)

                data = {key: self.dump(fields[key]) for key in fields}
                return {".metaid": str(type_id), ".fields": data}

            return None # pragma: no cover


class Unpacker:
    def unpack(self, src: object, __globals__=globals()):
        self._globals = __globals__
        if isinstance(src, dict):
            if src.get(".META") != None and src.get(".OBJ") != None:
                self.metatypes = {}
                self.proceeded = []
                self.metadict = src[".META"]
                return self.load(src[".OBJ"])
            else:
                return self.load(src)

        if is_none(src):
            return None

        if is_primitive(src):
            return src

        if isinstance(src, list):
            return [self.load(el) for el in src]

    def load(self, src, id_=None):
        if is_none(src):
            return None

        if is_primitive(src):
            return src

        elif isinstance(src, list):
            return [self.load(el) for el in src]


        elif isinstance(src, dict):
            if src.get(".metaid") != None and src.get(".metatype") == None:
                meta_id = src[".metaid"]
                obj = None

                if src[".metaid"] in self.proceeded:
                    obj = self.metatypes[meta_id]
                else:
                    obj = self.load(self.metadict[meta_id], meta_id)
                    self.metatypes[meta_id] = obj
                    self.proceeded.append(meta_id)
                if src.get(".fields"):
                    obj = create_instance(obj, self.load(src[".fields"]))
                return obj

            elif src.get(".metatype"):
                metatype = src[".metatype"]

                if metatype == "func":
                    if src[".module"] != "__main__":
                        try:
                            exec(f'from {src[".module"]} import {src[".name"]}')
                            return eval(f'{src[".name"]}')
                        except Exception:
                            pass

                    refs = self.load(src[".refs"])
                    nonlocals = refs[0]
                    globals_ = refs[1]

                    co_raw = self.load(src[".code"])

                    co = CodeType(
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

                    closures = tuple(cell_factory(nonlocals[el]) for el in co.co_freevars)

                    naked = [
                        co,
                        globals(),
                        src[".name"],
                        src[".defaults"],

                        closures
                    ]

                    func = FunctionType(*naked)
                    return func

                if metatype == "builtin-func": # pragma: no cover
                    try:
                        exec(f'from {src[".module"]} import {src[".name"]}')
                        return eval(f'{src[".name"]}')
                    except Exception:
                        raise KeyError(f'builtin func "{src[".module"]}.{src[".name"]}" import failed')

                elif metatype == "class":
                    if src[".module"] != "__main__":
                        try:
                            exec(f'from {src[".module"]} import {src[".name"]}')
                            return eval(f'{src[".name"]}')
                        except Exception:
                            pass

                    class_info = src[".class"]
                    mro = self.load(class_info["mro"])
                    cls = create_classbase(src[".name"], mro)

                    self.metatypes[id_] = cls
                    self.proceeded.append(id_)

                    attrs = self.load(class_info["attrs"])

                    return set_classattrs(cls, attrs)

                elif metatype == "module": # pragma: no cover
                    try:
                        exec(f'import {src[".name"]}')
                        result = eval(src[".name"])
                        return result
                    except Exception:
                        if ".code" in src.keys():
                            with open("{}/{}.py".format("/".join(modules["__main__"].__file__.split('/')[:-1]),
                                                        src[".name"]), "w") as writer:
                                writer.write(src[".code"])
                            exec(f'import {src[".name"]}')
                            result = eval(src[".name"])
                            os.unlink(
                                "{}/{}.py".format("/".join(modules["__main__"].__file__.split('/')[:-1]), src[".name"]))
                            return result
                    raise KeyError(f'module"{src[".module"]}" import failed')

                elif metatype == "builtin": # pragma: no cover
                    if src.get(".builtin"):
                        return getattr(builtins, src[".builtin"])
                    else:
                        raise KeyError(f'builtin "{src[".builtin"]}" import failed')

                else:
                    raise KeyError(f"Unexpected metatype: {metatype}")

            elif src.get(".collection_type"):
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

                return res
