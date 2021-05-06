from io import FileIO
from typing import Any, IO
from json import dumps, loads

from lib.packager import *


class JsonParser:  # pragma: no cover
    base_dumps = dumps
    base_loads = loads

    def dump(self, obj: object, file: object = None, unpacked=True) -> None: 
        if unpacked: 
            packed_obj = Packer().pack(obj)
        else: 
            packed_obj = obj
        if file:
            with open(file, 'w') as file:
                file.write(JsonParser.base_dumps(packed_obj))
        else:
            raise ValueError("File transfer aborted")

    def dumps(self, obj: object) -> None: 
        packed_obj = Packer().pack(obj)
        return JsonParser.base_dumps(packed_obj)

    def load(self, file: object, unpack=True) -> Any: 
        if file:
            with open(file, 'r') as file:
                raw_obj = JsonParser.base_loads(file.read())
            if unpack: 
                unpacked_obj = Unpacker().unpack(raw_obj)
                return unpacked_obj
            else: # pragma: no cover
                return raw_obj

        else: # pragma: no cover
            raise ValueError("File transfer aborted")

    def loads(self, json: str) -> Any: 
        raw_obj = JsonParser.base_loads(json)
        unpacked_obj = Unpacker().unpack(raw_obj)
        return unpacked_obj
