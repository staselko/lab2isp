from io import FileIO
import warnings
from typing import Any, IO
from yaml import dump, load
from lib.packager import *

warnings.filterwarnings("ignore")


class YamlParser: # pragma: no cover
    base_dumps = dump
    base_loads = load

    def dump(self, obj: object, file: object = None, unpacked=True):
        if unpacked:
            packed_obj = Packer().pack(obj)
        else:
            packed_obj = obj
        if file:
            with open(file, 'w') as file:
                file.write(YamlParser.base_dumps(packed_obj))
        else:
            raise ValueError("File transfer aborted")

    def dumps(self, obj: object):
        packed_obj = Packer().pack(obj)
        return YamlParser.base_dumps(packed_obj)

    def load(self, file: object, unpack=True):
        if file:
            with open(file, 'r') as file:
                raw_obj = YamlParser.base_loads(file.read())
            if unpack:
                unpacked_obj = Unpacker().unpack(raw_obj)
                return unpacked_obj
            else:
                return raw_obj
        else:
            raise ValueError("File transfer aborted")

    def loads(self, json: str):
        raw_obj = YamlParser.base_loads(json)
        unpacked_obj = Unpacker().unpack(raw_obj)
        return unpacked_obj
