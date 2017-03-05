############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Hao Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import collections
import copy
import time
############################################################
# Section 1: Sudoku
############################################################
def read_board(path):
    board = {}
    row = 0
    col = 0
    star_set = {1,2,3,4,5,6,7,8,9}
    txt = open(path)
    lines = txt.read().split()
    for line in lines:
        for char in line:
            if char == '*':
                board[(row, col)] = star_set
            else:
                board[(row, col)] = set([int(char)])
            col = (col + 1) % 9
        row = (row + 1) % 9
    return board


def sudoku_cells():
    cellList = []
    for row in xrange(9):
        for col in xrange(9):
            cellList.append((row,col))
    return cellList


def sudoku_arcs():
    arcList = []
    for row in xrange(9):
        for col in xrange(9):
            #row
            for i in xrange(9):
                arcList.append(((row,col), (row, i)))
            #col
            for j in xrange(9):
                arcList.append(((row,col), (j, col)))
            arcList.remove(((row,col), (row, col)))
            arcList.remove(((row,col), (row, col)))
            #block ??? how to determine which four
            if row in [0,3,6]:
                if col in [0,3,6]:
                    arcList.append(((row,col), (row+1, col+1)))
                    arcList.append(((row,col), (row+1, col+2)))
                    arcList.append(((row,col), (row+2, col+1)))
                    arcList.append(((row,col), (row+2, col+2)))
                if col in [1,4,7]:
                    arcList.append(((row,col), (row+1, col-1)))
                    arcList.append(((row,col), (row+1, col+1)))
                    arcList.append(((row,col), (row+2, col-1)))
                    arcList.append(((row,col), (row+2, col+1)))
                if col in [2,5,8]:
                    arcList.append(((row,col), (row+1, col-1)))
                    arcList.append(((row,col), (row+1, col-2)))
                    arcList.append(((row,col), (row+2, col-1)))
                    arcList.append(((row,col), (row+2, col-2)))

            if row in [1,4,7]:
                if col in [0,3,6]:
                    arcList.append(((row,col), (row-1, col+1)))
                    arcList.append(((row,col), (row-1, col+2)))
                    arcList.append(((row,col), (row+1, col+1)))
                    arcList.append(((row,col), (row+1, col+2)))
                if col in [1,4,7]:
                    arcList.append(((row,col), (row+1, col-1)))
                    arcList.append(((row,col), (row+1, col+1)))
                    arcList.append(((row,col), (row-1, col-1)))
                    arcList.append(((row,col), (row-1, col+1)))
                if col in [2,5,8]:
                    arcList.append(((row,col), (row+1, col-1)))
                    arcList.append(((row,col), (row+1, col-2)))
                    arcList.append(((row,col), (row-1, col-1)))
                    arcList.append(((row,col), (row-1, col-2)))

            if row in [2,5,8]:
                if col in [0,3,6]:
                    arcList.append(((row,col), (row-1, col+1)))
                    arcList.append(((row,col), (row-1, col+2)))
                    arcList.append(((row,col), (row-2, col+1)))
                    arcList.append(((row,col), (row-2, col+2)))
                if col in [1,4,7]:
                    arcList.append(((row,col), (row-1, col-1)))
                    arcList.append(((row,col), (row-1, col+1)))
                    arcList.append(((row,col), (row-2, col-1)))
                    arcList.append(((row,col), (row-2, col+1)))
                if col in [2,5,8]:
                    arcList.append(((row,col), (row-1, col-1)))
                    arcList.append(((row,col), (row-1, col-2)))
                    arcList.append(((row,col), (row-2, col-1)))
                    arcList.append(((row,col), (row-2, col-2)))
    return arcList


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()


    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[(cell)]


    def remove_inconsistent_values(self, cell1, cell2):
         

        if len(list(self.board[cell1])) > 1 or len(list(self.board[cell2])) > 1:
            if len(self.board[cell2]) > 1:
                return False
            else:
                value = list(self.board[cell2])[0]
                list_value = list(self.board[cell1])
                if value in list_value:
                    list_value.remove(value)
                    self.board[cell1] = set(list_value)
                    return True
        return False

    def solved(self):
        for cell in self.CELLS:
            if len(self.board[cell]) != 1:
                return False
        return True

    def infer_ac3(self):
        board_copy = ""
        while not self.solved() and self.board != board_copy:
            board_copy = copy.deepcopy(self.board)
            for arc in self.ARCS:
                self.remove_inconsistent_values(arc[0],arc[1])
        return False

    def find_block(self,row,col):
        block = 0
        if row in [0, 1, 2]:
            if col in [0, 1, 2]:
                block = 1
            if col in [3, 4, 5]:
                block = 2
            if col in [6, 7, 8]:
                block = 3
        if row in [3, 4, 5]:
            if col in [0, 1, 2]:
                block = 4
            if col in [3, 4, 5]:
                block = 5
            if col in [6, 7, 8]:
                block = 6
        if row in [6, 7, 8]:
            if col in [0, 1, 2]:
                block = 7
            if col in [3, 4, 5]:
                block = 8
            if col in [6, 7, 8]:
                block = 9
        return block

    def infer_improved(self):
        pass
        board_copy = ""
        while (not self.infer_ac3()) and (not self.solved()) and (self.board != board_copy):
            board_copy = copy.deepcopy(self.board)
            for cell1 in self.CELLS:
                if (len(list(self.board[cell1])) > 1):
                    good_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
                    row_set = set()
                    col_set = set()
                    block_set = set()
                    row = cell1[0]
                    col = cell1[1]
                    block = self.find_block(row, col)
                    for cell2 in self.CELLS:
                        block2 = self.find_block(cell2[0], cell2[1])
                        if cell2[0] == row and ((cell1), (cell2)) in self.ARCS:
                            row_set = row_set | self.board[cell2]
                        if cell2[1] == col and ((cell1), (cell2)) in self.ARCS:
                            col_set = col_set | self.board[cell2]
                        if block2 == block and ((cell1), (cell2)) in self.ARCS:
                            block_set = block_set | self.board[cell2]
               #     print cell1, "row set", row_set
                #    print cell1, "col set", col_set
                #    print cell1, "block set", block_set
                    if row_set != good_set:
                        target_value = good_set - row_set
             #           print "ROW:TARGET:", cell1, ",VALUE:", list(target_value)[0], "PERFORM UPDATE"
                        self.board[cell1] = target_value
                      #  board_copy = self.board

                        break
                    if col_set != good_set:
                        target_value = good_set - col_set

                    #   print "COL:TARGET:", cell1, ",VALUE:", list(target_value)[0], "PERFORM UPDATE"
                        self.board[cell1] = target_value
                     #   board_copy = self.board

                        break
                    if block_set != good_set:
                        target_value = good_set - block_set
                     #   print "BLO:TARGET:", cell1, ",VALUE:", list(target_value)[0], "PERFORM UPDATE"
                        self.board[cell1] = target_value
                     #   board_copy = self.board

                        break

      #  print "LOOPED"
        return False

    def valid(self):
        for arc1 in self.ARCS:
            value = self.board[arc1[0]]
            for arc2 in self.ARCS:
                if arc1[0] == arc2[0]:
                    if self.board[arc2[1]] == value:
                        return False
        return True

    def infer_helper(self, current):
        if current.solved() and current.valid():
            return True
        for points in current.CELLS:
            if len(list(current.board[points])) > 1:
                for value in list(current.board[points]):
                    child = copy.deepcopy(current)
                    child.board[points] = set([value])
                    child.infer_improved()
                    if not child.solved() or not child.valid():
                        continue
                    if self.infer_helper(child):
                        self.board = child.board
                        return True
        return False

    def infer_with_guessing(self):
        if not self.infer_improved():
            self.infer_helper(self)





    def print_board(self):
        counter = 0
        for cell in self.CELLS:
            if counter % 9 == 0:
                print ""
            print self.board[cell],
            counter = counter + 1

"""
sudoku = Sudoku(read_board("hw4-medium1.txt"))

start = time.time()
sudoku.infer_improved()
print time.time()-start

sudoku.print_board()
"""
############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
18 hours
"""

feedback_question_2 = """
Improving the performance is the most challenging part.
"""

feedback_question_3 = """
Giving more examples (sample output for a giving instruction) in the pdf for EACH function and sub function would be good.

"""
