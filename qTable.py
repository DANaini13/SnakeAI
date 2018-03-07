import numpy as np
import pandas as pd
from pathlib import Path


class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.3, e_greedy=0.9, max_status = 256):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float)
        self.max_status = max_status
        csvfile = Path("q_table.csv")
        if csvfile.exists():
            self.q_table = pd.read_csv("q_table.csv")
            self.q_table = self.q_table.set_index("Unnamed: 0")

    def choose_action(self, observation):
        self.check_state_exist(observation)
        if np.random.uniform() < self.epsilon:
            state_action = self.q_table.loc[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.idxmax()
        else:
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'Target':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()
        else:
            q_target = r 
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )
    
    def save_to_file(self):
        self.q_table.to_csv("q_table.csv")

    def print_table(self):
        print(len(self.q_table))