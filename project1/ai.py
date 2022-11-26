import json
from simulator import *
import random
import numpy as np
from gui import Graphic
import time
# *** you can change everything except the name of the class, the act function and the sensor_data ***


class Agent:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        self.solutions = []
        self.axis = {'X':0,"Y":1,"Z":2}
        self.degrees = {"90":1,'180':2,"270":3}
        

    # the act function takes a json string as input
    # and outputs an action string
    # action example: [1,2,-2]
    # the first number is the joint number (1: the first joint)
    # the second number is the axis number (0: x-axis, 1: y-axis, 2: z-axis)
    # the third number is the degree (1: 90 degree, -2: -180 degree, -1000: -90000 degree)
    def act(self, percept):
        # ^^^ DO NOT change the act function above ***

        sensor_data = json.loads(percept)
        # ^^^ DO NOT change the sensor_data above ***
        if self.solutions == []:
            initial_state = Simulator(sensor_data['coordinates'],sensor_data["stick_together"])
            valid_idxs = self.remove_unnecessary_cubes(initial_state)
            self.solutions = self.BFS(initial_state,valid_idxs)
            # self.solutions = self.IDS(initial_state,valid_idxs,10)
            # self.testing(initial_state)
        print(self.solutions)
        agent_action = self.solutions.pop()

        # convert to required format 
        action = [agent_action[0],]
        action.append(self.axis[agent_action[1][0]])
        action.append(self.degrees[agent_action[1][1:]])

        print(action)
        # action example: [1,2,-2]
        return action

    def remove_unnecessary_cubes(self,state):

        indexes = list(range(0,27))

        for cubes in state.sticky_cubes:
            indexes.remove(cubes[1])

        for idx in indexes:
            if self.is_linear(state,idx): 
                indexes.remove(idx)
        return indexes

    def is_linear(self,state:Simulator, agent_idx):

        if agent_idx == 0 or agent_idx == 26:
            return True

        loc_i = state.coordinates[agent_idx]

        loc_post = state.coordinates[agent_idx+1]
        loc_pre = state.coordinates[agent_idx-1]
        

        if (loc_i[0] == loc_pre[0] and loc_i[0] == loc_post[0] and loc_i[1] == loc_pre[1] and loc_i[1] == loc_post[1]):
            return not [agent_idx, agent_idx + 1] in state.sticky_cubes
        if (loc_i[0] == loc_pre[0] and loc_i[0] == loc_post[0] and loc_i[2] == loc_pre[2] and loc_i[2] == loc_post[2]):
            return not [agent_idx, agent_idx + 1] in state.sticky_cubes
        if (loc_i[2] == loc_pre[2] and loc_i[2] == loc_post[2] and loc_i[1] == loc_pre[1] and loc_i[1] == loc_post[1]):
            return not [agent_idx, agent_idx + 1] in state.sticky_cubes

        return False

    def BFS(self, initial_state: Simulator,valid_indexes:list):
        valid_indexes = list(range(0,27))
        
        interface = Interface()
        queue = []
        # append the first state as (state, action_history)
        queue.append([initial_state, []])
        
        while queue:
            # pop first element from queue
            game_state = queue.pop(0)
            # agent_idx = np.random.randint(0,27)
            # get the list of legal actions
            # actions_list = interface.valid_actions(game_state[0],agent_idx)
            # indexes = list(range(0,27))
            random.shuffle(valid_indexes)
            
            
            for agent_idx in valid_indexes :
            # randomizing the order of child generation
                actions_list = interface.valid_actions(game_state[0],agent_idx)
                random.shuffle(actions_list)
                # action = random.sample(actions_list,1)[0]
                for action in actions_list:
                    # copy the current state
                    child_state = interface.copy_state(game_state[0])
                    
                    # take action and change the copied node
                    interface.evolve(child_state, agent_idx,action)
                    
                    # add children to queue
                    queue.append([child_state, [(agent_idx,action)] + game_state[1]])
                    
                    # return if goal test is true
                    if interface.goal_test(child_state): return [(agent_idx,action)] + game_state[1]
    

    def IDS(self, initial_state:Simulator,valid_indexes, limit):
        solution = []
        interface = Interface()

        for i in range(limit):
            if self.DFS(initial_state,valid_indexes,i):
                return self.DFS(initial_state,valid_indexes,i)

        

    # def DFS(self,state:Simulator, interface:Interface,depth,actions = []):
        
    #     if depth == 0:
    #         return
        
    #     agent_idx = np.random.randint(0,27)
    #     actions_list = interface.valid_actions(state,agent_idx)
    #     random.shuffle(actions_list)
    #     for action in actions_list:
    #         child_state = interface.copy_state(state)
    #         self.DFS(child_state,interface,depth-1)
    #         interface.evolve(child_state, agent_idx,action)
    #         actions.append((agent_idx,action))
    #         if interface.goal_test(child_state):
    #             return [(agent_idx,action)] 
    def DFS(self, initial_state: Simulator,valid_indexes:list,depth):

        interface = Interface()
        queue = []
        # append the first state as (state, action_history)
        queue.append([initial_state, []])
        counter = 0
        while queue:

            game_state = queue.pop()
            random.shuffle(valid_indexes)
            

            for agent_idx in valid_indexes :
                actions_list = interface.valid_actions(game_state[0],agent_idx)
                random.shuffle(actions_list)
                
                for action in actions_list:
                    
                    child_state = interface.copy_state(game_state[0])
                    
                    interface.evolve(child_state, agent_idx,action)
                    queue.append([child_state, [(agent_idx,action)] + game_state[1]])
                    if interface.goal_test(child_state): return [(agent_idx,action)] + game_state[1]
            counter += 1
            if counter == depth:
                break

    def testing(self,state:Simulator):
        
        interface = Interface()
        gui = Graphic()
        if interface.goal_test(state):
            print('Done')
        solu_0 = [(3, 'Z90')]
        solution_3 = [(8, 'X180'), (2, 'X90'), (4, 'X270'), (0, 'Y180'), (13, 'X90'), (1, 'Z270'), (3, 'X270')]
        solution_2 =[(15, 'X90'), (9, 'Y270'), (6, 'X270'), (22, 'Z270'), (18, 'Z270'), (14, 'Z90')]
        solution_1 = [(20, 'Y90'), (14, 'X90')]
        solo = [(20, 'Z270'), (10, 'Z90'), (11, 'X270')]
        solution_5 = [(19, 'Z180'), (1, 'Y270'), (22, 'Y90'), (8, 'Z90'), (5, 'Y270')]
        solution_10 = [(19, 'Z270'), (13, 'X90')]
        for (agent_idx,action) in reversed(solu_0):
            
            
            # print(agent_idx,action)
            interface.evolve(state,agent_idx,action)
            if not interface.valid_state(state):
                raise('invalid')

            gui.display(state.coordinates)
            # time.sleep(1)