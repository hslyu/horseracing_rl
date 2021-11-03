#!/usr/bin/env python3

import numpy as np

class EpsilonGreedyPolicy:

    def __init__(self, epsilon):
        self.epsilon = epsilon

    def choose(self, agent):
        if np.random.random() < self.epsilon:
            return np.random.choice(len(agent.value_estimates))
        else:
            best_action = np.max(agent_value_estimates)
            tie = np.where(agent.value_estimates == agent.value_estimates[best_action])[0]
            return np.random.choice(tie)

class RandomPolicy(EpsilonGreedyPolicy):

    def __init__(self):
        super(RandomPolicy, self).__init__(1)

class UCBPolicy:
    def __init__(self, c):
        self.c = c

    def choose(self, agent):
        exploration = np.log(agent.t+1)/agent.action_attemps
        exploration[np.isnan(exploration)] = 0
        exploration = np.power(exploration, 1/self.c)

        q = agent.value_estimates + exploration
        best_action = np.argmax(q)
        tie = np.where(q == q[best_action])[0]

        return np.random.choice(tie)

if __name__=="__main__":
    p = EpsilonGreedyPolicy(1)
    p = RandomPolicy()
    p = UCBPolicy(1)
