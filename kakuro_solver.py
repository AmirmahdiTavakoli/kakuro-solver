# import CSP from csp
from game_entity import *


class Kakuro_solver:
    def __init__(self, puzzle):
        self.grid = list()
        self.rows = len(puzzle)
        self.cols = len(puzzle[0])
        self.set_grid(puzzle)
        self.variables = set()
        self.clues = set()
        self.default_domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.vertical_neighbor = dict()
        self.horizontal_neighbor = dict()
        self.neighbor = [self.horizontal_neighbor, self.vertical_neighbor]

    def set_grid(self, puzzle):
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                element = puzzle[i][j]
                position = Position(i, j)  # Create a Position object for the current cell
                if '\\' in element:
                    numbers = element.split('\\')
                    if numbers[0] == '':
                        self.grid[i].append(Clue(int(numbers[1]), 'horizontal', position))
                    elif numbers[1] == '':
                        self.grid[i].append(Clue(int(numbers[0]), 'vertical', position))
                    else:
                        self.grid[i].append([Clue(numbers[0], 'vertical', position),
                                             Clue(numbers[1], 'horizontal', position)])
                else:
                    if '' in element:
                        self.grid[i].append(Variable([], '', position))
                    else:
                        self.grid[i].append(element)
                        print("*")

    def is_complete(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if isinstance(self.grid[i][j], Variable) and self.grid[i][j].value == '':
                    return False
        return True

    def initialize_variables(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if isinstance(self.grid[i][j], Variable):
                    self.variables.add(self.grid[i][j])
                    self.update_variable_domain(i, j)

    def update_variable_domain(self, row, col):
        variable = self.grid[row][col]

        # Check vertical neighbors
        if row > 0 and isinstance(self.grid[row - 1][col], Variable):
            variable.domain = list(set(variable.domain) & set(self.grid[row - 1][col].domain))

        if row < self.rows - 1 and isinstance(self.grid[row + 1][col], Variable):
            variable.domain = list(set(variable.domain) & set(self.grid[row + 1][col].domain))

        # Check horizontal neighbors
        if col > 0 and isinstance(self.grid[row][col - 1], Variable):
            variable.domain = list(set(variable.domain) & set(self.grid[row][col - 1].domain))

        if col < self.cols - 1 and isinstance(self.grid[row][col + 1], Variable):
            variable.domain = list(set(variable.domain) & set(self.grid[row][col + 1].domain))

    def print_puzzle(self):
        for i in range(self.rows):
            for j in range(self.cols):
                element = self.grid[i][j]
                if isinstance(element, Variable):
                    print(element.value, end=' ')
                elif isinstance(element, Clue):
                    if element.direction == "horizontal":
                        print(f'X\\{element.value}', end=' ')
                    else:
                        print(f'{element.value}\\X', end=' ')
                elif isinstance(element, list):
                    print(f'{element[0].value}\\{element[1].value}', end=' ')
                else:
                    print(element, end=' ')
            print()  # Print a new line after each row

    def solve(self):
        self.initialize_variables()  # Initialize the variables and their domains
        assignment = {}
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        # Check if the puzzle is complete
        if self.is_complete():
            return assignment
            # Select an unassigned variable
            variable = self.select_unassigned_variable(assignment)

        # Iterate over the domain of the selected variable
        for value in variable.domain:
            # Assign the value to the variable
            variable.value = value

            # Check if the assignment is consistent
            if self.is_consistent(variable):
                # Recursively call backtrack on the updated assignment
                result = self.backtrack(assignment)
                if result is not None:
                    return result

            # Remove the assignment if it leads to failure
            variable.value = ''

        # Return failure (no solution)
        return None

    def select_unassigned_variable(self, assignment):
        # Simplest variable selection strategy: choose the next unassigned variable
        for variable in self.variables:
            if variable.position not in assignment:
                return variable

    def is_consistent(self, variable):
        # Check if the assignment is consistent
        # Check vertical neighbors
        row, col = variable.position.row, variable.position.col

        if row > 0 and isinstance(self.grid[row - 1][col], Variable):
            if self.grid[row - 1][col].value == variable.value:
                return False

        if row < self.rows - 1 and isinstance(self.grid[row + 1][col], Variable):
            if self.grid[row + 1][col].value == variable.value:
                return False

        # Check horizontal neighbors
        if col > 0 and isinstance(self.grid[row][col - 1], Variable):
            if self.grid[row][col - 1].value == variable.value:
                return False

        if col < self.cols - 1 and isinstance(self.grid[row][col + 1], Variable):
            if self.grid[row][col + 1].value == variable.value:
                return False

        # Check if the variable satisfies the clue constraints
        for clue in variable.clues:
            clue_sum = sum(self.grid[clue.position.row][clue.position.col].value for clue in variable.clues)
            if clue_sum > clue.value:
                return False

        return True
