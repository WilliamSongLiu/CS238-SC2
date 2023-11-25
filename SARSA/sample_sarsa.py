import numpy as np
import random
import json
from collections import defaultdict

#Load Jsonl data
with open('game1.jsonl', 'r') as file:
    data = [json.loads(line) for line in file]

#Flatten the states to store in Q-table
def flatten_state(state):
    flat_state = []
    for key, value in state.items():
        if isinstance(value, dict):
            flat_state.extend(value.values())
        else:
            flat_state.append(value)
    return tuple(flat_state)

#Join actions into a single action string
def action_to_string(actions):
    return '_'.join(actions)

#Define all possible actions
all_actions = [action_to_string(entry['actions_wanted']) for entry in data]
unique_actions = list(set(all_actions))

#Initialize Q-table
q_table = defaultdict(lambda: defaultdict(float))

#Define learning parameters
alpha = 0.1;    #learning rate
gamma = 0.9;    #discount factor
epsilon = 0.5;  #exploration rate

#SARSA Learning Loop
for entry in data:
    current_state = flatten_state(entry['s'])
    action = action_to_string(entry['actions_wanted'])
    reward = entry['r']

    #If a state has next state, update it's q value
    if 'sp' in entry:
        next_state = flatten_state(entry['sp'])

        #Epsilon-greedy policy for next action
        if np.random.uniform(0,1) < epsilon:
            next_action = random.choice(unique_actions)
        else:
            next_action = max(q_table[next_state], key=q_table[next_state].get, default=random.choice(unique_actions))

        #Sarsa update
        current_q_value = q_table[current_state][action]
        next_q_value = q_table[next_state][next_action]
        new_q_value = current_q_value + alpha*(reward + gamma*next_q_value - current_q_value)

    #If a state is terminal (no sp)
    else:
        #Sarsa update (next_q_value=0, future reward=0)
        new_q_value = reward
    
    #Update Q-table
    q_table[current_state][action] = new_q_value

#Derive a policy based on the Q-table
def derive_policy(q_table):
    policy = {}
    for state in q_table:
        best_action = max(q_table[state], key=q_table[state].get, default=random.choice(unique_actions))
        policy[state] = best_action

    return policy

#Policy of SARSA learning
policy = derive_policy(q_table)

#Converting actions back to original
def split_actions(action_string):
    #split the actions by underscore
    words = action_string.split('_')
    return ['_'.join(words[i:i+2]) for i in range(0, len(words), 2)]

#Write the policy to a .jsonl file
with open('policy_game1.jsonl', 'w') as file:
    for flat_state, action in policy.items():
        list_states = list(flat_state)
        list_actions = split_actions(action)

        policy_line = {"s":list_states, "a":list_actions}
        json_line = json.dumps(policy_line)
        file.write(json_line + '\n')