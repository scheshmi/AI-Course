import json


# *** you can change everything except the name of the class, the act function and the sensor_data ***


class Agent:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        pass

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

        # TODO implement your agent here

        # action example: [1,2,-2]
        return action
