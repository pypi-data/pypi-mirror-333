from onlyaml.err import perr_exit
from dacite import from_dict
from typing import Type, TypeVar


T = TypeVar("T")


class ReadonlyDict:
    def __init__(self, entries):
        self.records = dict(entries)

    def __getitem__(self, k):
        d = self.records
        if (k in d):
            v = d[k]
            if isinstance(v, dict):
                return ReadonlyDict(v)
            return d[k]
        else:
            perr_exit(
                '"{}" is not present at your config file, program exit'
                .format(k)
            )

    def __str__(self):
        return self.records.__str__()

    def __len__(self):
        return self.records.__len__()

    def to(self, dataclass: Type[T]) -> T:
        data = self.records
        return from_dict(dataclass, data)
