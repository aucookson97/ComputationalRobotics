"""
Week 1 Problem 1: 1D Discrete Dynamical System
"""

import random
import matplotlib.pyplot as plt

class State():
    
    def __init__(self, x, v):
        self.x = x # Position
        self.v = v # Velocity
        
class Environment():
    
    def __init__(self, initial_state, p_e):
        self.state = initial_state
        self.p_e = p_e
        self.time = 0
        self.history = [self.state.x] # History is just for graphing

    def time_step(self, acceleration, verbose=False):
        wind = self._update_state(acceleration)
        self.history.append(self.state.x)

        if verbose:
            print ('\nTime: {}'.format(self.time))
            print ('\tPosition: {}'.format(self.state.x))
            print ('\tVelocity: {}'.format(self.state.v))
            print ('\tWind: {}'.format(wind))
            self.visualize()

        self.time += 1
    
    def _update_state(self, acceleration):
        wind = random.choices((0, 1, -1), 
                              weights=(1-2*self.p_e, self.p_e, self.p_e), 
                              k=1)[0]
        self.state.v += acceleration + wind
        self.state.x += self.state.v
        return wind
        
    def visualize(self):
        plt.plot(self.history, 'o', color='black')
        plt.title('1D Point Mass Position Over Time')
        plt.xlabel('Time')
        plt.ylabel('Position')
        plt.show()

if __name__ == "__main__":
    p_e = .25 # Probability to change velocity by +-1
    initial_state = State(0, 0) # Initial position and velocity
    
    environment = Environment(initial_state, p_e)
    
    # Automatic
    num_iterations = 1000
    for _ in range(num_iterations):
        acceleration = random.randint(-1, 1)
        environment.time_step(acceleration)
    environment.visualize()
    
    # # User Input
    # while True:
    #     acceleration = int(input('Enter Acceleration: '))
    #     print (acceleration)
    #     if acceleration > 1 or acceleration < -1:
    #         print('Please enter either 0, 1, or -1 for acceleration')
    #     else:
    #         environment.time_step(acceleration)
        

