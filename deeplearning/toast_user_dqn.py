import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K

from deeplearning.toast_user_environment import UserEnvironment

iteration = 5000


class DQN:
    def __init__(self, _state_size, _action_size):
        self.state_size = _state_size
        self.action_size = _action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # 미래 보상 감가, discount rate
        self.epsilon = 1.0  # 새로운 탐색, exploration rate
        self.epsilon_min = 0.01
        self.epsion_decay = 0.99
        self.learning_rate = 0.001
        self.main_model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    # buffer에 저장
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    # Choose action with epsilon, state
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.main_model.predict(state)
        return np.argmax(act_values[0])

    # every c time, random sample from buffer and train main NN
    def replay_train(self, _batch_size):
        minibatch = random.sample(self.memory, _batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.main_model.predict(state)  # update 할 NN output
            if done:
                target[0][action] = reward
            else:
                target[0][action] = reward + self.gamma * np.max(self.target_model.predict(next_state)[0])
            self.main_model.fit(state, target)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsion_decay

    def update_target_model(self):
        # copy weights from model to target_model
        self.target_model.set_weights(self.main_model.get_weights())

    def load(self, name):
        self.main_model.load_weights(name)

    def save(self, name):
        self.main_model.load_weights(name)


if __name__ == "__main__":
    env = UserEnvironment()
    state_size = env.state_size
    action_size = env.action_size
    agent = DQN(state_size, action_size)
    done = False
    batch_size = 32

    for e in range(iteration):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        for time in range(500):
            action = agent.act(state)
            next_state = env.step(action)
            reward = 3  # 사용자로부터 불러오기
            done = False  # 사용자로부터 불러오기
            if done:
                reward = - 10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state

    if len(agent.memory) > batch_size:
        agent.replay_train(batch_size)
        agent.update_target_model()