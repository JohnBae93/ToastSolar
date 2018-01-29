'''
User label environment for DQN
'''

import numpy as np

belong_len = 29
property_len = 9

label_belong = []
label_property = []


class UserEnvironment:
    def __init__(self):
        self.state_size = belong_len + property_len
        self.action_size = (belong_len + property_len) * 3
        self.init_state = label_belong + label_property

    def reset(self):
        return self.init_state

    def step(self, state, action):
        # action : index of list length = total label length * 3 (minus, stay, plus), one-hot
        # [stat[0] + 0.05, state[0], stat[0] - 0.05, ....
        #           , state[n-1] + 0.05, state[n-1], state[n-1] - 0.5]
        new_state = self.update_state(state, action)
        return new_state

    def update_state(self, state, action):
        new_state = state

        alpha = 0
        if (action // 3) % 3 == 0:
            alpha = 0.05
        if (action // 3) % 3 == 2:
            alpha = -0.05

        new_state[action // 3] = new_state[action // 3] + alpha
        return new_state
