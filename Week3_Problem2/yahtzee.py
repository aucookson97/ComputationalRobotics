#!/usr/bin/env python
# coding: utf-8

# In[10]:


import random
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations_with_replacement


# In[ ]:





# In[133]:


class Yahtzee:
    def __init__(self, ):
        self.states = {}
        self.gamma=1
        self.action_masks = list(combinations_with_replacement([True,False],5))
        self.init_states()
        self.value_iteration(100)

    def value_iteration(self, max_iters):
        for i in range(max_iters):
            self.bellman_backup()
            if i % 10 == 0:
                print ('Iteration {}'.format(i))
        #plt.scatter()

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

            next_state_weighted_values = np.array([])

            for action in self.action_masks:
                action = np.array(action)
                reroll = current_state_dice[action]    # Dice we are rerolling
                store = current_state_dice[~action]    # Dice we are keeping

                prob_of_next_state = np.power(1/6,(5-len(reroll)))
                if len(reroll) == 0:
                    next_state = sorted(store)
                else:
                    rerolled = combinations_with_replacement([1,2,3,4,5,6], len(reroll))
                    for reroll_comb in rerolled:
                        if len(store) == 0:
                            next_state = sorted(reroll_comb)
                        else:
                            next_state = sorted(np.concatenate([reroll_comb, store])) # Concatenate stored dice with new dice
                        next_state.append(current_state_reroll+1)
                        next_state_weighted_values=                           np.append(next_state_weighted_values, prob_of_next_state*self.states[tuple(next_state)])
            self.states[s] = np.max(next_state_weighted_values)


# In[ ]:





# In[134]:


game = Yahtzee()


# In[46]:


print (game.score((4, 2, 1, 3, 6, 1)))


# In[100]:





# In[ ]:




