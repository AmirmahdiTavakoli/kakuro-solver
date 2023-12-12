class Substance:
    def __init__(self, position, type):
        self.position = position
        self.type = type


class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col


class Variable(Substance):
    def __init__(self, value, position, domain={}):
        self.clues = set()
        self.value = value
        self.domain = domain
        super().__init__(position, "Variable")

    def set_clues(self, clue):
        self.clues = clue


class Clue(Substance):
    def __init__(self, value, direction, position):
        self.value = value
        self.direction = direction
        self.length = None
        self.position = position
        self.variables = set()
        self.current_sum = 0
        super().__init__(position, "Clue")

    def set_variable(self, variable):
        self.variables.add(variable)
        self.length = len(variable)