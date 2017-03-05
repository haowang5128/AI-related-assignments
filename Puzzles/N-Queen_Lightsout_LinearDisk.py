############################################################
# CMPSC 442: Homework 2
############################################################

student_name = "Hao Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import random
import copy
############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):

    comb = (math.factorial(n*n))/((math.factorial(n))*(math.factorial(n*n-n)))
    return comb

def num_placements_one_per_row(n):

    return (n**n)

def n_queens_valid(board):

    depth = 0
    for i in board:
        for j in range (depth):
            if i == board[j] or i == board[j]+(depth-j) or i == board[j]-(depth-j):
                return False
        depth = depth + 1
    return True


def n_queens_solutions(n):

    def n_queens_helper(n, state = ()):

        for col in range(n):
            if (n_queens_valid(state+(col,))):
                if len(state) == n-1:
                    yield [col, ]

                else:
                    for result in n_queens_helper(n, state+(col,)):
                        yield [col, ] + result

    return list(n_queens_helper(n))

############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        
        self.board = board
    def get_board(self):
        
        return self.board
    def perform_move(self, row, col):
        

        size_row = len(self.board)-1
        size_col = len(self.board[row])-1

        if row == 0:
            if col == 0:
                self.board[row][col] = not self.board[row][col]
                self.board[row][col + 1] = not self.board[row][col + 1]
                self.board[row + 1][col] = not self.board[row + 1][col]

            elif col == size_col:
                self.board[row][col] = not self.board[row][col]
                self.board[row][col - 1] = not self.board[row][col - 1]
                self.board[row + 1][col] = not self.board[row + 1][col]
            else:
                self.board[row][col] = not self.board[row][col]
                self.board[row][col - 1] = not self.board[row][col - 1]
                self.board[row][col + 1] = not self.board[row][col + 1]
                self.board[row + 1][col] = not self.board[row + 1][col]

        elif row == size_row:
            if col == 0:
                self.board[row][col] = not self.board[row][col]
                self.board[row][col + 1] = not self.board[row][col + 1]
                self.board[row - 1][col] = not self.board[row - 1][col]

            elif col == size_col:
                self.board[row][col] = not self.board[row][col]
                self.board[row][col - 1] = not self.board[row][col - 1]
                self.board[row - 1][col] = not self.board[row - 1][col]
            else:
                self.board[row][col] = not self.board[row][col]
                self.board[row][col - 1] = not self.board[row][col - 1]
                self.board[row][col + 1] = not self.board[row][col + 1]
                self.board[row - 1][col] = not self.board[row - 1][col]

        elif col == 0:
            if row == 0:
                self.board[row][col] = not self.board[row][col]

                self.board[row][col + 1] = not self.board[row][col + 1]

                self.board[row + 1][col] = not self.board[row + 1][col]

            elif row == size_row:
                self.board[row][col] = not self.board[row][col]

                self.board[row][col + 1] = not self.board[row][col + 1]
                self.board[row - 1][col] = not self.board[row - 1][col]

            else:
                self.board[row][col] = not self.board[row][col]

                self.board[row][col + 1] = not self.board[row][col + 1]
                self.board[row - 1][col] = not self.board[row - 1][col]
                self.board[row + 1][col] = not self.board[row + 1][col]

        elif col == size_col:
            if row == 0:
                self.board[row][col] = not self.board[row][col]

                self.board[row][col - 1] = not self.board[row][col - 1]

                self.board[row + 1][col] = not self.board[row + 1][col]

            elif row == size_row:
                self.board[row][col] = not self.board[row][col]

                self.board[row][col - 1] = not self.board[row][col - 1]
                self.board[row - 1][col] = not self.board[row - 1][col]

            else:
                self.board[row][col] = not self.board[row][col]

                self.board[row][col - 1] = not self.board[row][col - 1]
                self.board[row - 1][col] = not self.board[row - 1][col]
                self.board[row + 1][col] = not self.board[row + 1][col]

        else:
            self.board[row][col] = not self.board[row][col]
            self.board[row][col + 1] = not self.board[row][col + 1]
            self.board[row][col - 1] = not self.board[row][col - 1]
            self.board[row - 1][col] = not self.board[row - 1][col]
            self.board[row + 1][col] = not self.board[row + 1][col]

    def scramble(self):
        
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (random.random() < 0.5):
                    self.perform_move(i,j)

    def is_solved(self):
        
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j]:
                    return False
        return True

    def copy(self):
        
        return copy.deepcopy(self)

    def successors(self):
        
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                successor = self.copy()
                successor.perform_move(i, j)
                yield ((i,j), successor)

    def find_solution(self):
        
        check_set = set()
        parent = {}
        moves = {}
        parent[self] = self
        moves[self] = (0,0)
        solution = []

        if self.is_solved():
            return moves[self]

        else:
            current = []
            current.append(self)

        check_set.add(tuple(tuple(i) for i in self.get_board()))

        while len(current) != 0:
            current_search = current.pop(0)
            if current_search.is_solved():
                    node = current_search
                    while(parent[node] != node):
                        solution.append(moves[node])
                        node = parent[node]
                    return list(reversed(solution))
            for move, neighbor in current_search.successors():
                if tuple(tuple(i) for i in neighbor.get_board()) not in check_set:
                    parent[neighbor] = current_search
                    moves[neighbor] = move
                    if neighbor.is_solved():
                        node = neighbor
                        while(parent[node] != node):
                            solution.append(moves[node])
                            node = parent[node]
                        return list(reversed(solution))
                    current.append(neighbor)
                    check_set.add(tuple(tuple(i) for i in neighbor.get_board()))
        return None

def create_puzzle(rows, cols):

    board = [[False for i in range(cols)] for j in range(rows)]
    return LightsOutPuzzle(board)


############################################################
# Section 3: Linear Disk Movement
############################################################
class Disk(object):
    def __init__(self, length, n, disk_list):
        self.length = length
        self.n = n
        self. disk_list = list(disk_list)

    def successor(self):
        i = 0
        li = self.disk_list
        while i < len(self.disk_list):
            if li[i] != 0:
                if i + 1 < self.length:
                    if li[i + 1] == 0:
                        temp = list(self.disk_list)
                        disk_to_move = temp[i]
                        temp[i] = 0
                        temp[i + 1] = disk_to_move
                        yield ((i, i + 1), Disk(self.length, self.n, temp))
                if i + 2 < self.length:
                    if li[i + 2] == 0 and li[i + 1] != 0:
                        temp = list(self.disk_list)
                        disk_to_move = temp[i]
                        temp[i] = 0
                        temp[i + 2] = disk_to_move
                        yield ((i, i + 2), Disk(self.length, self.n, temp))
                if i - 1 >= 0:
                    if li[i - 1] == 0:
                        temp = list(self.disk_list)
                        disk_to_move = temp[i]
                        temp[i] = 0
                        temp[i - 1] = disk_to_move
                        yield ((i, i - 1), Disk(self.length, self.n, temp))
                if i - 2 >= 0:
                    if li[i - 2] == 0 and li[i - 1] != 0:
                        temp = list(self.disk_list)
                        disk_to_move = temp[i]
                        temp[i] = 0
                        temp[i - 2] = disk_to_move
                        yield ((i, i - 2), Disk(self.length, self.n, temp))

            i = i+1

    def solved_identical(self):
        i = self.length - 1
        while i >= self.length - self.n:
            if self.disk_list[i] != 1:
                return False
            i =i-1
        return True

    def solved_distinct(self):
        i = self.length-1
        id = 1
        while id <= self.n:
            if self.disk_list[i] != id:
                return False
            i = i-1
            id = id+1
        return True

def solve_identical_disks(length, n):
    

    disk_list = []
    for disk in range (n):
        disk_list.append(1)
    for space in range (length-n):
        disk_list.append(0)

    identical = Disk(length, n, disk_list)
    moves = {}
    parent = {}
    check_set = set()
    solution = []
    parent[identical] = identical
    moves[identical] = ()
    current = []
    current.append(identical)
    check_set.add(tuple(identical.disk_list))

    if identical.solved_identical():
        return moves[identical]

    while len(current) != 0:
        current_search = current.pop(0)
        if current_search.solved_identical():
            node = current_search
            while (parent[node] != node):
                solution.append(moves[node])
                node = parent[node]
            return list(reversed(solution))
        for move, neighbor in current_search.successor():
            if tuple(neighbor.disk_list) not in check_set:
                parent[neighbor] = current_search
                moves[neighbor] = move
                if neighbor.solved_identical():
                    node = neighbor
                    while (parent[node] != node):
                        solution.append(moves[node])
                        node = parent[node]
                    return list(reversed(solution))
                check_set.add(tuple(neighbor.disk_list))
                current.append(neighbor)
    return None

def solve_distinct_disks(length, n):
    
    disk_list = []
    for disk in range (n):
        disk_list.append(1+disk)
    for space in range (length-n):
        disk_list.append(0)

    distinct = Disk(length, n, disk_list)
    moves = {}
    parent = {}
    check_set = set()
    solution = []
    parent[distinct] = distinct
    moves[distinct] = ()
    current = []
    current.append(distinct)
    check_set.add(tuple(distinct.disk_list))

    if distinct.solved_distinct():
        return moves[distinct]
        
    while len(current) != 0:
        current_search = current.pop(0)
        if current_search.solved_distinct():
            node = current_search
            while (parent[node] != node):
                solution.append(moves[node])
                node = parent[node]
            return list(reversed(solution))
        for move, neighbor in current_search.successor():
            if tuple(neighbor.disk_list) not in check_set:
                parent[neighbor] = current_search
                moves[neighbor] = move
                if neighbor.solved_distinct():
                    node = neighbor
                    while (parent[node] != node):
                        solution.append(moves[node])
                        node = parent[node]
                    return list(reversed(solution))
                check_set.add(tuple(neighbor.disk_list))
                current.append(neighbor)
    return None
############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
3 days
"""

feedback_question_2 = """
last two questions.
"""

feedback_question_3 = """
GUI part.
"""
