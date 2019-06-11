class DatabaseIndex(object):
    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __repr__(self):
        return f'({self.value}, {self.index})'
