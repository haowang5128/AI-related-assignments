############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Hao Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import copy
import Queue
import math
import time
############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    

    board = []
    row = []
    index = 1
    for i in xrange(rows):
        for j in xrange(cols):
            if (index == rows * cols):
                index = 0
                row.append(index)
            else:
                row.append(index)
                index = index+1

        board.append(row)
        row = []
    return TilePuzzle(board)

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        
        self.board = board
        self.row = len(board)
        self.col = len(board[0])
        for i in xrange(self.row):
            for j in xrange(self.col):
                if board[i][j] == 0:
                    self.empty_row = i
                    self.empty_col = j
                    self.empty = (self.empty_row, self.empty_col)


    def get_board(self):
        

        return self.board

    def perform_move(self, direction):
        

        if direction == "up":
            if self.empty_row == 0:
                return False
            self.board[self.empty_row][self.empty_col],self.board[self.empty_row - 1][self.empty_col] =  \
            self.board[self.empty_row - 1][self.empty_col], self.board[self.empty_row][self.empty_col]
            self.empty_row = self.empty_row - 1
            return True

        if direction == "down":
            if self.empty_row == self.row - 1:
                return False
            self.board[self.empty_row][self.empty_col], self.board[self.empty_row + 1][self.empty_col] = \
            self.board[self.empty_row + 1][self.empty_col], self.board[self.empty_row][self.empty_col]
            self.empty_row = self.empty_row + 1
            return True

        if direction == "left":
            if self.empty_col == 0:
                return False
            self.board[self.empty_row][self.empty_col], self.board[self.empty_row][self.empty_col - 1] = \
                self.board[self.empty_row][self.empty_col - 1], self.board[self.empty_row][self.empty_col]
            self.empty_col = self.empty_col - 1
            return True

        if direction == "right":
            if self.empty_col == self.col - 1:
                return False
            self.board[self.empty_row][self.empty_col + 1], self.board[self.empty_row][self.empty_col] = \
                self.board[self.empty_row][self.empty_col], self.board[self.empty_row][self.empty_col + 1]
            self.empty_col = self.empty_col + 1
            return True
        else:
            return False

    def scramble(self, num_moves):
        

        for i in xrange(num_moves):
            self.perform_move(random.choice(["up", "down", "left", "right"]))

    def is_solved(self):
        

        init = create_tile_puzzle(self.row, self.col)
        return self.get_board() == init.get_board()

    def copy(self):
        

        return copy.deepcopy(self)

    def successors(self):
        

        direction = ["up", "down", "left", "right"]
        for move in direction:
            copy = self.copy()
            if copy.perform_move(move):
                yield (move, copy)

    # Required

    def iddfs_helper(self, limit, moves):

        stack = []
        stack.append((self, 0))
        check_set = set()
        parent = {}
        parent[self] = self
        check_set.add(tuple(tuple(x) for x in self.get_board()))
        solution_set = []

        if self.is_solved():
            return solution_set
        while stack:
            current, depth = stack.pop()
            if depth < limit:
                for move, successor in current.successors():
                    if tuple(tuple(x) for x in successor.get_board()) not in check_set:
                        parent[successor] = current
                        moves[successor] = move

                        if successor.is_solved():
                            node = successor
                            solution = []
                            while (parent[node] != node):
                                solution.append(moves[node])
                                node = parent[node]
                            solution_set.append(list(reversed(solution)))
                        else:
                            stack.insert(0, (successor, depth + 1))
                            check_set.add(tuple(tuple(x) for x in successor.get_board()))
        return solution_set



    def find_solutions_iddfs(self):
        
        limit = 0
        moves = {}
        moves[self] = ""
        while True:
            solution = self.iddfs_helper(limit, moves)
            if solution:
                break
            else:
                limit = limit + 1

        for move in solution:
            yield move

    # Required
    def find_solution_a_star(self):
        

        queue = Queue.PriorityQueue()
        check_set = set()
        parent = {}
        parent[self] = self
        moves = {}
        moves[self] = ""
        queue.put((self.man_dis(), 0, self))
        check_set.add(tuple(tuple(x) for x in self.get_board()))
        solution = []

        while not queue.empty():
            current_entry = queue.get()
            current_puzzle = current_entry[2]
            g = current_entry[1]

            for move, successor in current_puzzle.successors():
                if tuple(tuple(x) for x in successor.get_board()) not in check_set:
                    parent[successor] = current_puzzle
                    moves[successor] = move
                    if successor.is_solved():
                        node = successor
                        while(parent[node] != node):
                            solution.append(moves[node])
                            node = parent[node]
                        return list(reversed(solution))
                    queue.put((successor.man_dis() + g + 1, g + 1, successor))
                    check_set.add(tuple(tuple(x) for x in successor.get_board()))

        return None


    def man_dis (self):
        dis_sum = 0
        for row in xrange(self.row):
            for col in xrange(self.col):
                current_tile = self.board[row][col]
                goal_row = self.find(current_tile, "row")
                goal_col = self.find(current_tile, "col")
                dis = abs(row - goal_row) + abs(col - goal_col)
                dis_sum = dis_sum + dis
        return dis_sum

    def find (self, tile, rorc):
        for row in xrange(self.row):
            for col in xrange(self.col):
                if tile == self.board[row][col]:
                    if rorc == "row":
                        return row
                    if rorc == "col":
                        return col

############################################################
# Section 2: Grid Navigation
############################################################


def find_path(start, goal, scene):
    

    queue = Queue.PriorityQueue()
    check_set = set()
    parent = {}
    parent[start] = start
    moves = {}
    moves[start] = start
    queue.put((euc_dis(start, goal), 0, start))
    check_set.add(start)
    solution = []

    while not queue.empty():
        current_entry = queue.get()
        current_point = current_entry[2]
        current_dis = current_entry[1]
        for successor in grid_successor(current_point, scene):
            if successor not in check_set:
                parent[successor] = current_point
                if successor == goal:
                    node = successor
                    while(parent[node] != node):
                        solution.append(node)
                        node = parent[node]
                    solution.append(node)
                    return list(reversed(solution))

                g = euc_dis(current_point, successor)
                queue.put((euc_dis(successor, goal) + current_dis + g, current_dis + g, successor))
                check_set.add(successor)
    return None



def euc_dis (current, goal):
    return math.sqrt ((current[0] - goal[0]) ** 2 + (current[1] - goal[1]) ** 2)

def grid_successor (point, scene):
    x = point[0]
    y = point[1]
    row = len(scene) -1
    col = len(scene[0]) -1
    print row, col
    #up
    if x - 1 >= 0 and scene[x - 1][y] == False:
        yield (x - 1, y)
    #down
    if x + 1 <= col and scene[x + 1][y] == False:
        yield (x + 1, y)
    #left
    if y - 1 >= 0 and scene[x][y - 1] == False:
        yield (x, y - 1)
    #right
    if y + 1 <= col and scene[x][y + 1] == False:
        yield (x, y + 1)
    #up left
    if x - 1 >= 0 and y - 1 >= 0 and scene[x - 1][y - 1] == False:
        yield (x - 1,y - 1)
    # up right
    if x - 1 >= 0 and y + 1 <= col and scene[x - 1][y + 1] == False:
        yield (x - 1, y + 1)
    # down left
    if x + 1 <= row and y - 1 >= 0 and scene[x + 1][y - 1] == False:
        yield (x + 1, y - 1)
    # down right
    if x + 1 <= row and y + 1 <= col and scene[x + 1][y + 1] == False:
        yield (x + 1, y + 1)



############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################
class Disk(object):

    def __init__(self, length, n, disk_list):
        self.length = length
        self.n = n
        self.disk_list = list(disk_list)
      #  print self.disk_list
        self.goal_list = []
        for space in xrange(length - n):
            self.goal_list.append(0)
        for disk in xrange(n):
            self.goal_list.append(n - disk)
     #   print self.goal_list
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

            i = i + 1

    def solved_distinct(self):
        i = self.length - 1
        id = 1
        while id <= self.n:
            if self.disk_list[i] != id:
                return False
            i = i - 1
            id = id + 1
        return True


    def cost(self):
        disk_list = self.disk_list
        goal_list = self.goal_list
        sum = 0
        for index in xrange(self.length):
            cost = abs(disk_list[index] - goal_list[index]) / 2
            sum = sum + cost
        return sum

def solve_distinct_disks(length, n):
    

    disk_list = []
    for disk in xrange(n):
        disk_list.append(1 + disk)
    for space in xrange(length - n):
        disk_list.append(0)

    distinct = Disk(length, n, disk_list)
    queue = Queue.PriorityQueue()
    check_set = set()
    parent = {}
    parent[distinct] = distinct
    moves = {}
    moves[distinct] = ()
    queue.put ((distinct.cost(),0, distinct))
    check_set.add(tuple(distinct.disk_list))
    solution = []


    while not queue.empty():
        current_entry = queue.get()
        current_disk = current_entry[2]
        g = current_entry[1]

        if current_disk.solved_distinct():
            node = current_disk
            while (parent[node] != node):
                solution.append(moves[node])
                node = parent[node]
            return list(reversed(solution))

        for move, successor in current_disk.successor():
            if tuple(successor.disk_list) not in check_set:
                parent[successor] = current_disk
                moves[successor] = move

                if successor.solved_distinct():
                    node = successor
                    while (parent[node] != node):
                        solution.append(moves[node])
                        node = parent[node]
                    return list(reversed(solution))
                queue.put((successor.cost() + g + 1, g + 1, successor))
                check_set.add(tuple(successor.disk_list))
    return None





#print solve_distinct_disks(5, 3)







############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    

    board = [[False for i in range(cols)] for j in range(rows)]
    return DominoesGame(board)

class DominoesGame(object):

    # Required
    num_leaf = 0

    def __init__(self, board):
        

        self.board = board
        self.row = len(board)
        self.col = len(board[0])

    def get_board(self):
        
        return self.board

    def reset(self):
        
        new_board = create_dominoes_game(self.row, self.col)
        self.board = new_board.get_board()

    def is_legal_move(self, row, col, vertical):
        

        if not vertical:
            if row <= self.row - 1 and col < self.col - 1 and self.board[row][col] == False and self.board[row][col + 1] == False:
                return True
            else:
                return False
        elif vertical:
            if row < self.row - 1 and col <= self.col - 1 and self.board[row][col] == False and self.board[row +1][col] == False:
                return True
            else:
                return False
        else:
            return False

    def legal_moves(self, vertical):
        

        for i in xrange(self.row):
            for j in xrange(self.col):
                if self.is_legal_move(i,j, vertical):
                    yield (i,j)

    def perform_move(self, row, col, vertical):
        

        self.board[row][col] = True
        if not vertical:
            self.board[row][col + 1] = True
        if vertical:
            self.board[row + 1][col] = True

    def game_over(self, vertical):
        
        moves = list(self.legal_moves(vertical))
        if moves:
            return False
        else:
            return True


    def copy(self):
        
        return copy.deepcopy(self)

    def successors(self, vertical):
        
        moves = list(self.legal_moves(vertical))
        for (i,j) in moves:
            copy = self.copy()
            copy.perform_move(i, j, vertical)
            yield ((i,j), copy)

    def get_random_move(self, vertical):
        
        moves = list(self.legal_moves(vertical))
        if moves:
          return random.choice(moves)
        else:
            return moves

    def evaluate(self, root):
        return len(list(self.legal_moves(root))) - len(list(self.legal_moves(not root)))

    def ABSearch(self, depth, alpha, beta, vertical, root, playermax):
        if depth == 0 or self.game_over(vertical):
            DominoesGame.num_leaf = DominoesGame.num_leaf + 1
            return ((0, 0), self.evaluate(root))
        if playermax:
            value = float("-inf")
            required_move = tuple()
            for move, successor in self.successors(vertical):
                position, temp = successor.ABSearch(depth - 1, alpha, beta, not vertical, root, False)
                if temp > value:
                    value = temp
                    required_move = move
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return (required_move, value)
        else:
            value = float("inf")
            required_move = tuple()
            for move, successor in self.successors(vertical):
                position, temp = successor.ABSearch(depth - 1, alpha, beta, not vertical, root, True)
                if temp < value:
                    value = temp
                    required_move = move
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return (required_move, value)
    # Required
    def get_best_move(self, vertical, limit):
        
        move, value = self.ABSearch(limit, float("-inf"), float("inf"), vertical, vertical, True)
        temp = DominoesGame.num_leaf
        DominoesGame.num_leaf = 0
        return move, value, temp


#print len(solve_distinct_disks(18,15))




############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
2 weeks
"""

feedback_question_2 = """
Speed up my functions
"""

feedback_question_3 = """
Gui part.
"""
