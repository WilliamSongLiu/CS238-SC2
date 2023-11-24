import numpy as np
import pandas as pd
import json

#JSON data sample
jason_data = 

#Parse JSON data
data = json.loads(json_data)

#Define states

#Define all possible actions
Actions = ["act_unit", "build_gas", "expand", "grid_building"]
num_actions = len(Actions)

#Initialize Q-table
q_table = {}

#Define learning parameters
alpha = 0.1;    #learning rate
gamma = 0.9;    #discount factor
epsilon = 0.1;  #exploration rate

#Get Q-value for a state-action pair
def get_q_value(state, action):
    return q_table.get((tuple(state), action), 0)

#Learning Loop
for i in range(len(data) -1):
    current_state = tuple(data[i]['State'])
    next_state = tuple(data[i+1]['State'])
    action = Actions.index(data[i]['Action'])
    reward = data[i]['Reward']

    #Epsilon-greedy policy for next action
    if np.random.uniform(0,1) < epsilon:
        next_action = np.random.choioce(num_actions)
    else:
        next_action = np.argmax([get_q_value(next_state, a) for a in range(num_actions)])

    #Sarsa update
    current_q_value = get_q_value(current_state, action)
    next_q_value = get_q_value(next_state, next_action)
    new_q_value = current_q_value + alpha*(reward + gamma*next_q_value - current_q_value)
    q_table[(current_state, action)] = new_q_value

def derive_policy(q_table, states, num_actions):
    policy = {}
    for state in states:
        best_action = np.argmax([q_table.get((state, action), 0) for action in range(num_actions)])
        policy[state] = best_action

    return policy