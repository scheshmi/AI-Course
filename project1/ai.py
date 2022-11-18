import json
from simulator import *
import random
import numpy as np
# *** you can change everything except the name of the class, the act function and the sensor_data ***


class Agent:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        self.solutions = []
        self.axis = {'X':0,"Y":1,"Z":2}
        self.degrees = {"90":1,'180':2,"270":3}
        print('ggg')

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
            self.solutions = self.BFS_SAMPLE_CODE(initial_state)
        
        agent_action = self.solutions.pop()

        # convert to required format 
        action = [agent_action[0],]
        action.append(self.axis[agent_action[1][0]])
        action.append(self.degrees[agent_action[1][1:]])

        print(action)
        # action example: [1,2,-2]
        return action

    def BFS_SAMPLE_CODE(self, initial_state: Simulator):
        
        interface = Interface()
        queue = []
        # append the first state as (state, action_history)
        queue.append([initial_state, []])

        while queue:
            # pop first element from queue
            game_state = queue.pop(0)
            agent_idx = np.random.randint(0,27)
            # get the list of legal actions
            actions_list = interface.valid_actions(game_state[0],agent_idx)
            
            # randomizing the order of child generation
            random.shuffle(actions_list)
            
            for action in actions_list:
                # copy the current state
                child_state = interface.copy_state(game_state[0])
                
                # take action and change the copied node
                interface.evolve(child_state, agent_idx, action)
                
                # add children to queue
                queue.append([child_state, [(agent_idx,action)] + game_state[1]])
                
                # return if goal test is true
                if interface.goal_test(child_state): return [(agent_idx,action)] + game_state[1]