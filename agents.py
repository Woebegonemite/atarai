# Author Lewis Stuart 201262348

import torch
import random

# Ensures that the results will be the same (same starting random seed each time)
random.seed(0)


# Handles what actions to take in the environment
class Agent():
    def __init__(self, strategy, num_actions):
        # The strategy for choosing which action to take
        self.strategy = strategy

        # Number of actions of the current game
        self.num_actions = num_actions
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Chooses the new action to take for the agent
    def select_action(self, state, policy_net, episode):

        # Returns the current exploration rate for the episode
        rate = self.strategy.get_exploration_rate(episode)

        # Chooses a random action if agent decides to explore
        if rate > random.random():
            return self.select_random_action()

        # Chooses the most optimal action, exploiting the neural network
        else:
            return self.select_exploitative_action(state, policy_net)

    # Returns random action
    def select_random_action(self):
        action = random.randrange(self.num_actions)
        return torch.tensor([action]).to(self.device)

    # Returns optimal action
    def select_exploitative_action(self, state, policy_net):
        with torch.no_grad():
            return policy_net(state).argmax(dim=1).to(self.device)  # exploit

    # Returns the default action (which is always 0)
    def select_default_action(self):
        return torch.tensor([0]).to(self.device)

    # Returns the current exploration rate
    def return_exploration_rate(self, episode):
        return self.strategy.get_exploration_rate(episode)