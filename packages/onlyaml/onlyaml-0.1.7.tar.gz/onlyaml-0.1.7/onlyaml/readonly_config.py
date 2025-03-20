from .err import perr_exit


class ReadonlyDict:
    def __init__(self, entries):
        self.records = dict(entries)

    def __getitem__(self, k):
        d = self.records
        if (k in d):
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
