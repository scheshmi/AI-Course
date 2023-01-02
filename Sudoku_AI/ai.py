import json
from sudoku import Sudoku,display
import random
from copy import deepcopy
import math
import numpy as np

class AI:

    def __init__(self):
        pass

    def solve(self, problem):
       
        problem_data = json.loads(problem)
        print("Initial Sudoku:")
        init_sudoku = np.array(problem_data['sudoku'])
        display(init_sudoku)

        repeat = 10
        init_sudoku = np.reshape(init_sudoku,(1,-1)).squeeze(axis=0)
        for rpt in range(repeat):
            print(f'Repetition: {rpt + 1} ')
            sudoku = deepcopy(init_sudoku)
            best_solver, best_score = Simulated_Annealing_Solver(sudoku)

            if best_score == -162:
                print("\nSudoku Solved.")
                break

        print("\nFinal Sudoku:")
        result = np.reshape(best_solver.sudoku,(9,9))
        display(result)

        final_json = json.dumps({"sudoku": result.tolist()})

        return final_json


def Simulated_Annealing_Solver(initial_sudoku,max_iter=300_000,patience_iters = 50_000):

    solver = Sudoku(initial_sudoku)
    solver.random_filling_zeros()
    best_solver = deepcopy(solver)
    current_score = solver.compute_score()
    best_score = current_score
    T = .5
    count = 0

    for iter in range(max_iter):
            
        if (iter % 1000 == 0): 
            print(f'Iteration: {iter}, Score: {current_score}')
        
        candidate_sudoku = solver.make_candidate_sudoku()
        solver_candidate = Sudoku(candidate_sudoku,solver.fixed_entries)
        candidate_score = solver_candidate.compute_score()
        delta_S = float(current_score - candidate_score)
        
        if (math.exp((delta_S/T)) - random.random() > 0):

            solver = solver_candidate
            current_score = candidate_score 
    
        if (current_score < best_score):
            best_solver = deepcopy(solver)
            best_score = best_solver.compute_score()
            count = 0
        else:
            count+=1
        
        if count == patience_iters:
            break
    
        if candidate_score == -162:
            solver = solver_candidate
            break

        T = 0.99999*T
    
    return best_solver, best_score