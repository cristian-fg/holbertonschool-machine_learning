#!/usr/bin/env python3
"""Q-learning"""
import numpy as np
epsilon_greedy = __import__('2-epsilon_greedy').epsilon_greedy


def train(env, Q, episodes=5000, max_steps=100,
          alpha=0.1, gamma=0.99, epsilon=1,
          min_epsilon=0.1, epsilon_decay=0.05):
    """performs Q-learning

    Args:
    -> env is the FrozenLakeEnv instance
    -> Q is a numpy.ndarray containing the Q-table
    -> episodes is the total number of episodes to train over
    -> max_steps is the maximum number of steps per episode
    -> alpha is the learning rate
    -> gamma is the discount rate
    -> epsilon is the initial threshold for epsilon greedy
    -> min_epsilon is the minimum value that epsilon should decay to
    -> epsilon_decay is the decay rate for updating epsilon between episodes
    -> When the agent falls in a hole, the reward should be updated to be -1

    Returns: Q, total_rewards
        * Q is the updated Q-table
        * total_rewards is a list containing the rewards per episode
    """
    rewards_all_episodes = []
    for episode in range(episodes):
        env.reset()
        reward = 0
        done = False
        state = 0

        for step in range(max_steps):
            A = epsilon_greedy(Q, state, epsilon)
            new_state, reward, done, _ = env.step(A)
            if done and reward == 0:
                reward -= 1

            Q[state, A] = Q[state, A] * (1 - alpha) + \
                alpha * (reward + gamma * np.max(Q[new_state]))

            state = new_state

            if done is True:
                break

        epsilon = max(epsilon * (1 - epsilon_decay), min_epsilon)

        rewards_all_episodes.append(reward)

    return Q, rewards_all_episodes
