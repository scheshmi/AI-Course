from copy import deepcopy
import json
import numpy as np


class Simulator:
    def __init__(self, coordinates, sticky_cubes):
        self.coordinates = coordinates
        self.sticky_cubes = sticky_cubes


    def take_action(self,agent_idx, action):

        tmp_coordiante = deepcopy(self.coordinates)
        # if agent_idx == 0 or agent_idx == 26:
        #     return

        if not self.is_sticky(agent_idx) and self.is_linear(agent_idx):
            return
            
        if self.is_sticky(agent_idx):
            # idx = agent_idx

            # while [idx, idx + 1] in self.sticky_cubes and self.is_linear(idx):
            #     idx += 1
            # if not self.is_linear(idx):
            #     #  take action on idx + 1 ..... 26
            #     sub_coordinates = self.coordinates[:idx+1]
            #     for i in range(idx + 1, 27):

            #         new_coordinate = self.do_action(idx, i, action)

            #         if new_coordinate not in sub_coordinates:
            #             # update coordinate
            #             self.coordinates[i] = new_coordinate
            #         else:
            #             self.coordinates = tmp_coordiante
            #             return

            idx = agent_idx
            
            # while [idx - 1, idx] in self.sticky_cubes and self.is_linear(idx):
                # idx -= 1
            if self.is_linear(idx):
                #  take action on 0 ..... idx -1
                # sub_coordinates = self.coordinates[idx+1:]
                sub_coordinates = self.coordinates[0:idx+1]

                for i in range(idx+1, 27):

                    new_coordinate = self.do_action(idx, i, action)

                    if new_coordinate not in sub_coordinates:
                        # update coordinate
                        self.coordinates[i] = new_coordinate
                    else:
                        self.coordinates = tmp_coordiante
                        return
        if not self.is_linear(agent_idx):
            
            if 'X' in action:
                if self.coordinates[agent_idx + 1][0] == self.coordinates[agent_idx][0]:
                    # i + 1 ..... 27 X degree rotation
                    sub_coordinates = self.coordinates[:agent_idx+1]
                    for i in range(agent_idx + 1, 27):

                        new_coordinate = self.do_action(
                            agent_idx, i, action)

                        if new_coordinate not in sub_coordinates:
                            # update coordinate
                            self.coordinates[i] = new_coordinate
                        else:
                            self.coordinates = tmp_coordiante
                            return

                else:
                    # 0 .... i-1 X degree rotation
                    sub_coordinates = self.coordinates[agent_idx:]
                    for i in range(0, agent_idx):

                        new_coordinate = self.do_action(
                            agent_idx, i, action)

                        if new_coordinate not in sub_coordinates:
                            # update coordinate
                            self.coordinates[i] = new_coordinate
                        else:
                            self.coordinates = tmp_coordiante
                            return

            elif 'Y' in action:
                if self.coordinates[agent_idx + 1][1] == self.coordinates[agent_idx][1]:
                    # i + 1 ..... 27 Y degree rotation
                    sub_coordinates = self.coordinates[:agent_idx+1]
                    for i in range(agent_idx + 1, 27):

                        new_coordinate = self.do_action(
                            agent_idx, i, action)

                        if new_coordinate not in sub_coordinates:
                            # update coordinate
                            self.coordinates[i] = new_coordinate
                        else:
                            self.coordinates = tmp_coordiante
                            return
                else:
                    # 0 .... i-1 y degree rotation
                    sub_coordinates = self.coordinates[agent_idx:]
                    for i in range(0, agent_idx):

                        new_coordinate = self.do_action(
                            agent_idx, i, action)

                        if new_coordinate not in sub_coordinates:
                            # update coordinate
                            self.coordinates[i] = new_coordinate
                        else:
                            self.coordinates = tmp_coordiante
                            return
            elif 'Z' in action:
                if self.coordinates[agent_idx + 1][2] == self.coordinates[agent_idx][2]:
                    # i + 1 ..... 27 z degree rotation
                    sub_coordinates = self.coordinates[:agent_idx+1]
                    for i in range(agent_idx + 1, 27):

                        new_coordinate = self.do_action(
                            agent_idx, i, action)

                        if new_coordinate not in sub_coordinates:
                            # update coordinate
                            self.coordinates[i] = new_coordinate
                        else:
                            self.coordinates = tmp_coordiante
                            return
                else:
                    # 0 .... i-1 z degree rotation
                    sub_coordinates = self.coordinates[agent_idx:]
                    for i in range(0, agent_idx):

                        new_coordinate = self.do_action(
                            agent_idx, i, action)

                        if new_coordinate not in sub_coordinates:
                            # update coordinate
                            self.coordinates[i] = new_coordinate
                        else:
                            self.coordinates = tmp_coordiante
                            return

        

    def is_sticky(self, agent_idx):
        # if agent_idx == 26:
        #     return [agent_idx - 1, agent_idx] in self.sticky_cubes
        # if agent_idx == 0:
        #     return [agent_idx, agent_idx+1] in self.sticky_cubes
        return ([agent_idx, agent_idx+1] in self.sticky_cubes) #or ([agent_idx - 1, agent_idx] in self.sticky_cubes)

    def is_linear(self, agent_idx):

        if agent_idx == 0 or agent_idx == 26:
            return True

        loc_i = self.coordinates[agent_idx]

        loc_post = self.coordinates[agent_idx+1]
        loc_pre = self.coordinates[agent_idx-1]
        

        if (loc_i[0] == loc_pre[0] and loc_i[0] == loc_post[0] and loc_i[1] == loc_pre[1] and loc_i[1] == loc_post[1]):
            return True
        if (loc_i[0] == loc_pre[0] and loc_i[0] == loc_post[0] and loc_i[2] == loc_pre[2] and loc_i[2] == loc_post[2]):
            return True
        if (loc_i[2] == loc_pre[2] and loc_i[2] == loc_post[2] and loc_i[1] == loc_pre[1] and loc_i[1] == loc_post[1]):
            return True

        return False

    def do_action(self, agent_idx, cube_idx, action):

        agent_coordinate = self.coordinates[agent_idx]
        cube_coordinate = self.coordinates[cube_idx]
        new_coordinate = self.compute_new_coordinate(
            agent_coordinate, cube_coordinate, action)

        return new_coordinate

    def compute_new_coordinate(self, agent_coordinate, cube_coordinate, action):
        if '180' in action:
            axis = action[0]
            if axis == "X":
                new_coordinate = [cube_coordinate[0], 0, 0]
                new_coordinate[1] = 2 * \
                    agent_coordinate[1] - cube_coordinate[1]
                new_coordinate[2] = 2 * \
                    agent_coordinate[2] - cube_coordinate[2]
            if axis == "Y":
                new_coordinate = [0, cube_coordinate[1], 0]
                new_coordinate[0] = 2 * \
                    agent_coordinate[0] - cube_coordinate[0]
                new_coordinate[2] = 2 * \
                    agent_coordinate[2] - cube_coordinate[2]
            if axis == "Z":
                new_coordinate = [0, 0, cube_coordinate[2]]
                new_coordinate[1] = 2 * \
                    agent_coordinate[1] - cube_coordinate[1]
                new_coordinate[0] = 2 * \
                    agent_coordinate[0] - cube_coordinate[0]

        if '90' in action:
            axis = action[0]
            if axis == "X":
                new_coordinate = [cube_coordinate[0], 0, 0]
                new_coordinate[1] = agent_coordinate[2] - \
                    cube_coordinate[2] + agent_coordinate[1]
                new_coordinate[2] = cube_coordinate[1] - \
                    agent_coordinate[1] + agent_coordinate[2]
            if axis == "Y":
                new_coordinate = [0, cube_coordinate[1], 0]
                new_coordinate[0] = -agent_coordinate[2] + \
                    cube_coordinate[2] + agent_coordinate[0]
                new_coordinate[2] = -cube_coordinate[0] + \
                    agent_coordinate[0] + agent_coordinate[2]
            if axis == "Z":
                new_coordinate = [0, 0, cube_coordinate[2]]
                new_coordinate[1] = cube_coordinate[0] - \
                    agent_coordinate[0] + agent_coordinate[1]
                new_coordinate[0] = agent_coordinate[1] - \
                    cube_coordinate[1] + agent_coordinate[0]
            

        if '270' in action:
            axis = action[0]
            if axis == "X":
                new_coordinate = [cube_coordinate[0], 0, 0]
                new_coordinate[1] = cube_coordinate[2] - \
                    agent_coordinate[2] + agent_coordinate[1]
                new_coordinate[2] = agent_coordinate[1] - \
                    cube_coordinate[1] + agent_coordinate[2]
            if axis == "Y":
                new_coordinate = [0, cube_coordinate[1], 0]
                new_coordinate[0] = -cube_coordinate[2] + \
                    agent_coordinate[2] + agent_coordinate[0]
                new_coordinate[2] = -agent_coordinate[0] + \
                    cube_coordinate[0] + agent_coordinate[2]
            if axis == "Z":
                new_coordinate = [0, 0, cube_coordinate[2]]
                new_coordinate[1] = agent_coordinate[0] - \
                    cube_coordinate[0] + agent_coordinate[1]
                new_coordinate[0] = cube_coordinate[1] - \
                    agent_coordinate[1] + agent_coordinate[0]
        return new_coordinate


class Interface:

    def __init__(self):
        pass

    def evolve(self, state: Simulator,agent_idx, action):
        if type(action) is not str:
            raise ("action is not a string")
        action = action.upper()
        if action not in self.valid_actions(state,agent_idx):
            raise ("action is not valid")
        state.take_action(agent_idx,action)
        

    def copy_state(self, state):

        _copy = Simulator(None, None)
        _copy.coordinates = deepcopy(state.coordinates)
        _copy.sticky_cubes = state.sticky_cubes
        return _copy

    def perceive(self, state):

        return json.dumps({'coordinates': state.coordinates, 'stick_together': state.sticky_cubes})

    def goal_test(self, state):

        maxs = np.max(state.coordinates, axis=0)
        max_x, max_y, max_z = maxs[0], maxs[1], maxs[2]

        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(0, 3):
                    cordinate = [max_x - i, max_y - j, max_z-k]
                    if cordinate not in state.coordinates:
                        return False
        return True

    def valid_actions(self, state: Simulator, agent_idx):
        valid_acts = ['X90', 'X270', 'X180', 'Y90',
                      'Y270', 'Y180', 'Z90', 'Z270', 'Z180']
        

        if agent_idx == 26:
            coordinate_26 = state.coordinates[26]
            coordinate_25 = state.coordinates[25]
            if (coordinate_26[2]== coordinate_25[2]):
                return ['Z90', 'Z270', 'Z180']
            if (coordinate_26[1]== coordinate_25[1]):
                return ['Y90', 'Y270', 'Y180']
            if (coordinate_26[0]== coordinate_25[0]):
                return ['X90', 'X270', 'X180']

        if agent_idx == 0:
            coordinate_0 = state.coordinates[0]
            coordinate_1 = state.coordinates[1]

            if (coordinate_0[2]== coordinate_1[2]):
                return ['Z90', 'Z270', 'Z180']
            if (coordinate_0[1]== coordinate_1[1]):
                return ['Y90', 'Y270', 'Y180']
            if (coordinate_0[0]== coordinate_1[0]):
                return ['X90', 'X270', 'X180']

        loc_i = state.coordinates[agent_idx]
        loc_post = state.coordinates[agent_idx+1]
        loc_pre = state.coordinates[agent_idx-1]

        if (loc_i[0] == loc_pre[0] and loc_i[0] == loc_post[0] and loc_i[1] == loc_pre[1] and loc_i[1] == loc_post[1]):
            return ['Z90', 'Z270', 'Z180']
        if (loc_i[0] == loc_pre[0] and loc_i[0] == loc_post[0] and loc_i[2] == loc_pre[2] and loc_i[2] == loc_post[2]):
            return ['Y90', 'Y270', 'Y180']
        if (loc_i[2] == loc_pre[2] and loc_i[2] == loc_post[2] and loc_i[1] == loc_pre[1] and loc_i[1] == loc_post[1]):
            return ['X90', 'X270', 'X180']

        if (loc_i[1] == loc_pre[1] and loc_i[1] == loc_post[1]):
            return ['Z90', 'Z270', 'Z180', 'X90', 'X270', 'X180']
        if (loc_i[0] == loc_pre[0] and loc_i[0] == loc_post[0]):
            return ['Y90', 'Y270', 'Y180', 'Z90', 'Z270', 'Z180']
        if (loc_i[2] == loc_pre[2] and loc_i[2] == loc_post[2]):
            return ['X90', 'X270', 'X180', 'Y90', 'Y270', 'Y180']

        return valid_acts

    def valid_state(self, state):
        axs = state.coordinates
        return len(np.unique(axs, axis=0)) == len(axs)