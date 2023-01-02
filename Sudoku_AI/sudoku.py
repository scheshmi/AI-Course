import numpy as np
import random
from copy import deepcopy

class SudokuSolver():
    def __init__(self, sudoku,fixed_entries=None):
        
        self.sudoku = sudoku
        
        if fixed_entries is None:
            self.fixed_entries = np.arange(81)[self.sudoku > 0]
        else:
            self.fixed_entries = fixed_entries
        
            
    def random_filling_zeros(self):
        for num in range(9):
            block_indices = self.get_block_indices(num)
            block = self.sudoku[block_indices]
            zero_indices = [idx for i,idx in enumerate(block_indices) if block[i] == 0]
            to_fill = [i for i in range(1,10) if i not in block]
            random.shuffle(to_fill)
            for i, value in zip(zero_indices, to_fill):
                self.sudoku[i] = value
            
    def get_block_indices(self, n, ignore_fixed=False):
        row = (n // 3) * 3
        col = (n % 3)  * 3
        indices = [col + (i%3) + 9*(row + (i//3)) for i in range(9)]
        
        if ignore_fixed:
            indices = filter(lambda x:x not in self.fixed_entries, indices)
        return list(indices)
        
    def get_column_indices(self, i):
        column = i
        indices = [column + 9 * j for j in range(9)]
        return indices
        
    def get_row_indices(self, i,):
        
        row = i
        indices = [j + 9*row for j in range(9)]
        return indices
        
    def compute_score(self):
        score = 0
        for row in range(9):
            score -= len(set(self.sudoku[self.get_row_indices(row)]))
        for col in range(9):
            score -= len(set(self.sudoku[self.get_column_indices(col)]))
        return score
        
    def make_candidate_sudoku(self):
        new_sudoku = deepcopy(self.sudoku)
        
        non_zero_block = []

        for blk in range(9):
            num_in_block = len(self.get_block_indices(blk, ignore_fixed=True))
            if num_in_block != 0:
                non_zero_block.append(blk)

        block = random.sample(non_zero_block,1)[0]
        num_in_block = len(self.get_block_indices(block, ignore_fixed=True))
        random_squares = random.sample(range(num_in_block),2)
        square_1, square_2 = [self.get_block_indices(block, ignore_fixed=True)[idx] for idx in random_squares]
        new_sudoku[square_1], new_sudoku[square_2] = new_sudoku[square_2], new_sudoku[square_1]
        return new_sudoku

def display(grid):
    
    for i in range(9):
        row = ""
        if i % 3 == 0:
            print("="*21)
        for j in range(9):
            if j % 3 == 0 and j > 0:
                row += "| "
            row += "-" if grid[i, j] == 0 else str(grid[i, j])
            row += " "
        print(row)
    print("="*21)
