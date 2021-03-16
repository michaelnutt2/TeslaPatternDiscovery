import pandas as pd
# using OpenAI Gym's environment
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random
from gym import spaces

operations = pd.read_csv('newops.csv', sep=',', header=None)


# Custom Env for VortexMath
class VortexMathEnv(Env):
    def __init__(self, inputs, output, q_table=None, rand_limit=None, rand_limit_output=None):
        # Define Discrete Actions
        # Example Action: digital root of 1,2 or three of the digits within a given integer,
        # and then either adding, subtracting, or multiply it.
        # Define 3 actions

        self.input = inputs

        digits = [[0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]
        self.possible = []
        for i in self.input:
            for d in digits:
                o = 0
                for n in d:
                    o += int(str(i)[n])
                if o > 9:
                    o = int(str(o)[0]) + int(str(o)[1])
                if not (o in self.possible):
                    self.possible.append(o)
        print(self.possible)

        self.possible_ops = []
        for p in self.possible:
            for x in range(4):
                self.possible_ops.append(p * 4 + x)

        print(self.possible_ops)
        self.action_space = Discrete(len(self.possible_ops))
        print(self.action_space)
        # Output Boundary -> 0 to output
        # self.observation_space = spaces.Tuple(Box(low=np.array([0]), high=np.array([output])),Discrete(83) )

        self.factor = 100

        features = {
            'position': Box(low=np.array([0]), high=np.array([self.factor * 2])),
            'operations': Discrete(40)
        }

        self.observation_space = spaces.Dict(features)
        print(self.observation_space)
        # Set Start State to 0
        self.state = 1
        self.state_norm = 0.0
        # Length of operations
        self.opCount = 0
        self.memory = []
        self.output = output
        self.reward = 0.0

        if rand_limit is None:
            self.rand_limit = self.factor
            self.rand_limit_output = int(self.output * (self.factor + self.rand_limit) / (self.factor))
        else:
            self.rand_limit = rand_limit
            self.rand_limit_output = rand_limit_output
        if q_table is None:
            self.q_table = pd.DataFrame(0.0, range(self.factor + self.rand_limit + 1), columns=range(40))
        else:
            self.q_table = q_table
        print(self.output)
        print(self.rand_limit_output)
        print(self.q_table)

    @classmethod
    def copy(cls, class_instance, inputs, output):
        q_table = class_instance.q_table.copy(deep=True)
        rand_limit = class_instance.rand_limit
        rand_limit_output = class_instance.rand_limit_output

        return cls(inputs, output, q_table, rand_limit, rand_limit_output)

    def step(self, action):
        '''
          # Apply action
          if action == 0:
              # apply actions/operations here
              print("call action method 1")
          elif action == 1:
              # apply actions/operations here
              print("call action method 2")
          elif action == 2:
              # apply actions/operations here
              print("call action method 3")
        '''
        done = False

        state_norm_previous = int((self.state / self.output) * self.factor)
        previous_state = self.state

        action_func = reusable_operation_function(operations.iloc[action], self.factor, self.state_norm, self.state,
                                                  self.output)
        self.state = action_func(self.input, self.state, self.memory)
        # print("action_func")

        self.opCount += 1
        opCount = self.opCount

        self.state_norm = int((self.state / self.output) * self.factor)

        if self.state_norm > (self.factor + self.rand_limit):
            self.state = previous_state
            self.state_norm = state_norm_previous
            self.q_table.iloc[state_norm_previous][operations.iloc[action][0]] -= 0.1 * (
                    (previous_state / self.output) + \
                    0.8 * (self.q_table.iloc[self.state_norm].max()) - self.q_table.iloc[state_norm_previous][
                        operations.iloc[action][0]])

        if self.state < 0:
            self.state = previous_state
            self.state_norm = state_norm_previous
            self.q_table.iloc[state_norm_previous][operations.iloc[action][0]] -= 0.1 * (
                    (previous_state / self.output) + \
                    0.8 * (self.q_table.iloc[self.state_norm].max()) - self.q_table.iloc[state_norm_previous][
                        operations.iloc[action][0]])

        if previous_state < self.output and self.state < self.output:
            self.reward += (self.state / self.output) + (self.state / self.output - previous_state / self.output)
            self.q_table.iloc[state_norm_previous][operations.iloc[action][0]] += 0.01 * (
                    (self.state / self.output) + (self.state / self.output - previous_state / self.output) + \
                    0.8 * (self.q_table.iloc[self.state_norm].max()) - self.q_table.iloc[state_norm_previous][
                        operations.iloc[action][0]])
        else:
            self.reward += (self.rand_limit_output / self.output) - (self.state / self.output) + (
                    previous_state / self.output - self.state / self.output)
            self.q_table.iloc[state_norm_previous][operations.iloc[action][0]] += 0.01 * (
                    (self.rand_limit_output / self.output) - (self.state / self.output) + (
                    previous_state / self.output - self.state / self.output) + \
                    0.8 * (self.q_table.iloc[self.state_norm].max()) - self.q_table.iloc[state_norm_previous][
                        operations.iloc[action][0]])

        # Calculate reward
        if self.state == self.output:
            done = True

            self.reward = self.reward / (self.opCount ** 2)
            # print(self.q_table)
            # self.reward = 100

        # Check if operations are completed
        # if self.opCount >= 50:
        #    done = True

        # Return step information
        # required by open ai
        info = {}
        return self.state, self.reward, done, info

    def static_step(self, action):
        '''
          # Apply action
          if action == 0:
              # apply actions/operations here
              print("call action method 1")
          elif action == 1:
              # apply actions/operations here
              print("call action method 2")
          elif action == 2:
              # apply actions/operations here
              print("call action method 3")
        '''
        done = False

        state_norm_previous = int((self.state / self.output) * self.factor)
        previous_state = self.state

        action_func = reusable_operation_function(operations.iloc[action], self.factor, self.state_norm, self.state,
                                                  self.output)
        self.state = action_func(self.input, self.state, self.memory)

        self.opCount += 1
        opCount = self.opCount

        self.state_norm = int((self.state / self.output) * self.factor)

        if self.state_norm > (self.factor + self.rand_limit):
            # print("Hit cap")
            self.state = previous_state
            self.state_norm = state_norm_previous

        if self.state < 0:
            self.state = previous_state
            self.state_norm = state_norm_previous

        # print(state_norm_previous)
        print(self.state_norm)
        # print(operations.iloc[action][0])
        # print(self.q_table.iloc[state_norm_previous][operations.iloc[action][0]])
        # print(time_part.max())

        if previous_state < self.output:
            self.reward += (self.state / self.output) + (self.state / self.output - previous_state / self.output)

        else:
            self.reward += (self.rand_limit_output / self.output) - (self.state / self.output) + (
                    previous_state / self.output - self.state / self.output)

        # Calculate reward
        if self.state == self.output:
            done = True

            self.reward = self.reward / self.opCount
            # print(self.q_table)
            # self.reward = 100

        # Check if operations are completed
        # if self.opCount >= 50:
        #    done = True

        # Return step information
        # required by open ai
        info = {}
        return self.state, self.reward, done, info

    def render(self):
        # no view required
        pass

    def reset(self):
        # Reset state to 0.
        self.state = 1
        # Reset operations
        self.operations = 0
        self.reward = 0
        self.opCount = 0
        self.memory = []
        return self.state


def reusable_operation_function(operation, factor, state_norm, state, output):
    operator = ''
    # print(operation)
    if state_norm < factor or state_norm > factor:
        if operation[2] == 0:
            operator = '+'
        elif operation[2] == 1:
            operator = '-'
        elif operation[2] == 2:
            operator = '*'
        else:
            operator = '/'  #
    elif state > output:
        # print("clamping minus")
        # print("State ", state)
        if operation[2] == 0:
            operator = '-'
        elif operation[2] == 1:
            operator = '-'
        elif operation[2] == 2:
            operator = '-'
        else:
            operator = '-'  #
    elif state < output:
        # print("clamping addition")
        # print("State ", state)
        if operation[2] == 0:
            operator = '+'
        elif operation[2] == 1:
            operator = '+'
        elif operation[2] == 2:
            operator = '+'
        else:
            operator = '+'  #

    def func(inP, state, memory):
        value = operation[1]
        if operator == '/' and value == 0:
            state = int(eval(str(state) + operator + str(1)))
        else:
            # print("Im dying here")
            state = int(eval(str(state) + operator + str(value)))
        memory.append(operation[0])
        return state

    return func


def digital_root(i, d):
    o = 0
    for n in d:
        o += int(str(i)[n])
    if o > 9:
        o = int(str(o)[0]) + int(str(o)[1])
    return o
