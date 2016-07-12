from random import randint

# Dynamic Aggregated Binary Tree
class DABTree():

    def __init__(self, branch=None, value=0.0):
        self.value = value
        self.branch = branch
        self.west = None
        self.east = None

    def add_value(self, value=1.0):
        self.add_leafward(value=value)
        if self.branch:
            self.branch.add_rootward(value=value)

    def add_rootward(self, value):
        self.value += value
        if self.branch:
            self.branch.add_rootward(value=value)
        assert(self.value == self.west.value + self.east.value)

    def add_leafward(self, value):
        self.value += value
        if self.west:
            assert(self.east)
            self.west.add_leafward(value=value/2.0)
            self.east.add_leafward(value=value/2.0)
            assert(self.value == self.west.value + self.east.value)

    def invoke_west(self):
        if not self.west:
            self.west = DABTree(branch=self, value=self.value/2.0)
            self.east = DABTree(branch=self, value=self.value/2.0)
        return self.west

    def invoke_east(self):
        if not self.east:
            self.west = DABTree(branch=self, value=self.value/2.0)
            self.east = DABTree(branch=self, value=self.value/2.0)
        return self.east

    def invoke_least(self):
        west = self.invoke_west()
        east = self.invoke_east()
        if west.value > east.value:
            return east
        if east.value > west.value:
            return west
        if randint(0, 1):
            return east
        return west
