import random
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations_with_replacement,product

class Yahtzee:
    def __init__(self, ):
        self.states = {}
        self.gamma=1
        self.action_masks = list(product([True,False],repeat=5))
        self.init_states()
        self.value_iteration(70,0.1)

    def value_iteration(self, max_iters,epsilon):
        for i in range(max_iters):
            print ('Iteration {}'.format(i))
            prev_values = list(self.states.values())
            self.bellman_backup()
            value_difference = np.subtract(list(self.states.values()),prev_values)
            if np.linalg.norm(value_difference,ord=np.inf)<= epsilon:
                print('Converged')
                return

        #plt.scatter()
    def get_optimal_policy_from_value(self,state):
        assert sorted(state)==state,"Input needs to be sorted"
        current_state_dice = np.array(state[:-1])
        current_state_reroll = state[-1]
        if current_state_reroll==3:
            return "No possible action when reroll count is 3."

        action_values = []
        for action in self.action_masks:
                next_state_weighted_values = 0
                action = np.array(action)
                reroll = current_state_dice[action]    # Dice we are rerolling
                store = current_state_dice[~action]    # Dice we are keeping

                prob_of_next_state = np.power(1/6,(len(reroll)))
                if len(reroll) == 0:
                    next_state = sorted(store)
                    next_state.append(current_state_reroll+1)
                    next_state_weighted_values = self.states[tuple(next_state)]

                else:
                    rerolled = combinations_with_replacement([1,2,3,4,5,6], len(reroll))
                    for reroll_comb in rerolled:
                        if len(store) == 0:
                            next_state = sorted(reroll_comb)
                        else:
                            next_state = sorted(np.concatenate([reroll_comb, store])) # Concatenate stored dice with new dice
                        next_state.append(current_state_reroll+1)
                        next_state_weighted_values+=self.gamma*prob_of_next_state*self.states[tuple(next_state)]
                action_values.append(next_state_weighted_values)
        max_action = np.argmax(action_values)
        return self.action_masks[max_action]

    def init_states(self):
        """ Initialize dictionary map of states to values
        Each state has 5 dice {0-6} and 1 reroll {1-3}
        """
        dice_comb = list(combinations_with_replacement([1,2,3,4,5,6], 5))
        for reroll in range(1, 4):
            for dice in dice_comb:
                state = tuple(sorted(dice) + [reroll])
                self.states[state] = 0 if reroll != 3 else self.score(state)

    def score(self, state):
        """
            YAHTZEE (5 of a kind) is worth 50 points
            Otherwise the score is the highest sum of the same number
        """
        state = state[:-1]
        if len(np.unique(state)) == 1: # YAHTZEE!
            return 50

        best_score = 0
        for num in np.unique(state):
            score = num * state.count(num)
            best_score = max(best_score, score)

        return best_score

    def bellman_backup(self):
        for s, v in self.states.items():
            current_state_dice = np.array(s[:-1])
            current_state_reroll = s[-1]
            if current_state_reroll==3:
                continue

            action_values = []


            for action in self.action_masks:
                next_state_weighted_values = 0
                action = np.array(action)
                reroll = current_state_dice[action]    # Dice we are rerolling
                store = current_state_dice[~action]    # Dice we are keeping

                prob_of_next_state = np.power(1/6,(len(reroll)))
                if len(reroll) == 0:
                    next_state = sorted(store)
                    next_state.append(current_state_reroll+1)
                    next_state_weighted_values = self.states[tuple(next_state)]

                else:
                    rerolled = combinations_with_replacement([1,2,3,4,5,6], len(reroll))
                    for reroll_comb in rerolled:
                        if len(store) == 0:
                            next_state = sorted(reroll_comb)
                        else:
                            next_state = sorted(np.concatenate([reroll_comb, store])) # Concatenate stored dice with new dice
                        next_state.append(current_state_reroll+1)
                        next_state_weighted_values+=self.gamma*prob_of_next_state*self.states[tuple(next_state)]
                action_values.append(next_state_weighted_values)
            self.states[s] = np.max(action_values)

game = Yahtzee()
first_roll = [game.states[x] for x in game.states if x[-1]==1]
print('The estimated value of the starting state is {}.'.format(np.mean(first_roll)))
print(game.get_optimal_policy_from_value((1,1,1,2,4,1))) #True means to reroll, False means to keep