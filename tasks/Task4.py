import copy

class Vector:
    def __init__(self, init_list):
        if isinstance(init_list, list):
            self.list = copy.deepcopy(init_list)
            self.dimension = len(self.list)
        else:
            if isinstance(init_list, Vector):
                self.list = copy.deepcopy(init_list.list)
                self.dimension = len(self.list)
            else:
                raise TypeError("list or Vector expected but not {}".format(type(init_list)))

    def __eq__(self, value):
        if not (isinstance(value, list) or isinstance(value, Vector)):
            raise TypeError("list or Vector expected but not {}".format(type(value)))
        if isinstance(value, list):
            for el in value:
                if not (isinstance(el, int) or isinstance(el, float)):
                    raise TypeError("Float or int objects are supported, not {}".format(type(el)))
        if self.dimension != len(value):
            return False
        for i in range(len(value)):
                if self.list[i] != value[i]:
                    return False
        return True

    def __len__(self):
        return self.dimension

    def __add__(self, other):
        if not (isinstance(other, list) or isinstance(other, Vector)):
            raise TypeError("list or Vector expected but not {}".format(type(other)))
        if isinstance(other, list):
            for el in other:
                if not (isinstance(el, int) or isinstance(el, float)):
                    raise TypeError("Float or int objects are supported, not {}".format(type(el)))
        if self.dimension != len(other):
            raise ValueError("Dimensions are not equal")
        result = Vector(self.list)
        for i in range(len(other)):
            result[i] = result[i] + other[i]
        return result

    def __sub__(self, other):
        if not (isinstance(other, list) or isinstance(other, Vector)):
            raise TypeError("list or Vector expected but not {}".format(type(other)))
        if isinstance(other, list):
            for el in other:
                if not (isinstance(el, int) or isinstance(el, float)):
                    raise TypeError("Float or int objects are supported, not {}".format(type(el)))
        if self.dimension != len(other):
            raise ValueError("Dimensions are not equal")
        result = Vector(self.list)
        for i in range(len(other)):
            result[i] = result[i] - other[i]
        return result

    def __mul__(self, other):
        """Notice that u can only use Vectot*scalar but not vice versa"""
        if (isinstance(other, int) or isinstance(other, float)):
            result = Vector(self.list)
            for el in result:
                el *= other
            return result
        if not (isinstance(other, list) or isinstance(other, Vector)):
            raise TypeError("list or Vector expected but not {}".format(type(other)))
        if isinstance(other, list):
            for el in other:
                if not (isinstance(el, int) or isinstance(el, float)):
                    raise TypeError("Float or int objects are supported, not {}".format(type(el)))
        if self.dimension != len(other):
            raise ValueError("Dimensions are not equal")
        result = 0
        for i in range(len(other)):
            result += self.list[i] * other[i]
        return result

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.list[key % len(self.list)]
        else:
            raise KeyError("key in Vector.__getitem__(key) should be int")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.list[key % len(self.list)] = value
        else:
            raise KeyError("key in Vector.__getitem__(key) should be int")

    def __str__(self):
        return str(self.list)

    def norm(self):
        return sum([el**2 for el in self.list])