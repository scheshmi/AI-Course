# from sklearn.decomposition import PCA
import json
import numpy as np
from functools import lru_cache
from scipy.spatial.transform import Rotation
import sys


@lru_cache()
def rotation_matrix(axi, degree90):
    r = Rotation.from_euler({0: 'x', 1: 'y', 2: 'z'}[axi], 90 * degree90, degrees=True)
    return r.as_matrix().T.astype(int)


class Simulator:
    def __init__(self, coordinates, stick_together=None):
        if coordinates is None: return
        self.coordinates=np.array(coordinates).astype(int)

        self.stick_together = [[i[0]-1,i[1]-1] for i in stick_together]
        self.effective_axis, self.effective_bead = self.find_effective_axis()
        self.real_joints = np.array([i for i in self.effective_bead if i is not None])

    def find_bead_info(self):
        joint_list = np.diff(np.diff(self.coordinates, axis=0), axis=0)
        joint_list = np.arange(1, len(joint_list) + 1)[~(joint_list == [0, 0, 0]).all(axis=1)]

        stick_ranges=[]
        i=0
        while len(self.stick_together) > i:
            a=self.stick_together[i][0]
            b=self.stick_together[i][1]
            j=i+1
            while j!=len(self.stick_together) and b==self.stick_together[j][0]:
                b=self.stick_together[j][1]
                j+=1
            stick_ranges.append(list(range(a,b+1)))
            i=j

        is_joint, stick_beads, possible_axi = [], [], []
        for i in range(len(self.coordinates)):
            is_joint.append(i in joint_list)
            temp = [a for a in stick_ranges if i in a]
            stick_beads.append([] if len(temp)==0 else temp[0])
            if i == 0 or i == len(self.coordinates) - 1:
                possible_axi.append([False, False, False])
                continue
            possible_axi.append((self.coordinates[i + 1] - self.coordinates[i - 1]) != 0)

        return is_joint, stick_beads, possible_axi, joint_list

    def find_effective_axis(self):
        is_joint, stick_beads, possible_axi, joint_list = self.find_bead_info()
        effective_rotations=[]
        effective_bead = []
        for i in range(len(self.coordinates)):
            before_stick = [a for a in stick_beads[i] if a < i]
            before_stick = before_stick[::-1]
            after_stick = [a for a in stick_beads[i] if a > i]

            joint_before = any(j in joint_list for j in before_stick)
            joint_after = any(j in joint_list for j in after_stick)
            joint_current = is_joint[i]

            if not joint_current and (joint_before == joint_after):
                effective_rotations.append([False, False, False])
                effective_bead.append(None)
                continue
            if joint_current and not joint_after and not joint_before:
                effective_rotations.append(possible_axi[i])
                effective_bead.append(i)
                continue
            if joint_current and joint_before and joint_after:
                effective_rotations.append([False, False, False])
                effective_bead.append(None)
                continue

            side_sticks = [before_stick, after_stick][int(joint_after)]
            for closest_stick_joint in side_sticks:
                if is_joint[closest_stick_joint]: break

            if not joint_current:
                effective_rotations.append(possible_axi[i])
                effective_bead.append(closest_stick_joint)
                continue

            if joint_current:
                effective_rotations.append(possible_axi[i])
                block_index=np.argmax(
                    (self.coordinates[closest_stick_joint]-self.coordinates[i])!=0)
                effective_rotations[-1][block_index]=False
                effective_bead.append(i)
                continue

        return np.array(effective_rotations), np.array(effective_bead)

    def take_action(self, joint_num, axi, degree90):
        if not self.effective_axis[joint_num][axi]: return
        joint_num=self.effective_bead[joint_num]

        self.coordinates=self.coordinates-self.coordinates[joint_num]

        if joint_num>12:
            self.coordinates[joint_num+1:]= \
                self.coordinates[joint_num+1:]@rotation_matrix(axi, degree90%4)
        else:
            self.coordinates[:joint_num]= \
                self.coordinates[:joint_num]@rotation_matrix(axi, (-degree90)%4)

    # def __eq__(self, other):
    #     mat1 = self.coordinates - self.coordinates[0]
    #     mat2 = other.coordinates - other.coordinates[0]
    #     return (PCA().fit_transform(mat1) == PCA().fit_transform(mat2)).all()


class Interface:
    def __init__(self):
        pass

    def evolve(self, state, action):
        state.take_action(*action)

    def copy_state(self, state):
        _copy = Simulator(None)

        _copy.coordinates = np.copy(state.coordinates)
        _copy.effective_axis = state.effective_axis
        _copy.effective_bead = state.effective_bead
        _copy.real_joints = state.real_joints
        return _copy

    def perceive(self, state):
        return json.dumps({"coordinates": state.coordinates.tolist(),
                           "stick_together": state.stick_together})

    def goal_test(self, state):
        axs = state.coordinates.T
        if abs(np.unique(axs[0], return_counts=True)[1]-9).sum()!=0 or \
                abs(np.unique(axs[1], return_counts=True)[1]-9).sum()!=0 or \
                abs(np.unique(axs[2], return_counts=True)[1]-9).sum()!=0:
            return False
        return True

    def valid_actions(self, state, prev_joints):
        # return [(joint, axi, degree90), ...]
        joints = state.real_joints[[not i in prev_joints for i in state.real_joints]]
        axi = [0, 1, 2]
        degree = [1, 2, 3]
        # a = np.transpose([np.tile(joints, len(axi)), np.repeat(axi, len(joints))])
        res=[]
        for i in joints:
            for j in axi:
                for k in degree:
                    res.append([i,j,k])
        # np.random.shuffle(res)
        return res

    def valid_state(self, state):
        axs = state.coordinates
        return len(np.unique(axs, axis=0)) == len(axs)


def test_one_problemset(sample_input_json):
    game = Simulator(sample_input_json['coordinates'], sample_input_json['stick_together'])
    interface = Interface()
    from ai import Agent
    agent = Agent()

    action_count = 0
    while not (interface.goal_test(game)):
        action = agent.act(interface.perceive(game))
        interface.evolve(game, action)
        if not interface.valid_state(game): raise 'reached invalid state'
        action_count += 1
    return action_count


with open(r"problem_set.txt", 'r') as fp: res=eval(fp.read())
cost=test_one_problemset(res[int(sys.argv[1])])
print(cost, file=sys.stdout)