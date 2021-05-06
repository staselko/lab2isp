import json

def attrsource(obj, file):
    setattr(obj, "__attrsource__", file)
    print(obj.__dict__)
    return obj

class FieldFetcherMeta(type):
    def __new__(cls, *args):
        obj = super(FieldFetcherMeta, cls).__new__(cls, *args)
        with open(FieldFetcherMeta.__attrsource__, "r") as reader:
            attribute_string = reader.read()
        attr_dict = json.loads(attribute_string)
        for attr in attr_dict:
            setattr(obj, attr, attr_dict[attr])
        return obj

class Some(metaclass=attrsource(FieldFetcherMeta, "src/attrdump.json")):
    pass