from typing import Any, Collection, Iterable
from copy import deepcopy as dc

class CollectionFormater:
    def __init__(self, collection: Iterable):
        self.iterable = collection
        self.counter = 0

    def __iter__(self):
        return self.iterable.__iter__()

    def select(self, func: bool(Any)):
        self.counter += 1
        return self._preselect(func) 

    def _preselect(self, func: bool(Any)):
        print(self.counter)
        new_col = dc(CollectionFormater(self.iterable))
        for el in self.iterable:
            if not func(self.iterable.__getitem__(el)):
                del new_col.iterable[el]
        return new_col