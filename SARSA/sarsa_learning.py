import numpy as np
import random
import json
import os
from collections import defaultdict

#Define inpath for .jsonl and outpath for policy
in_path = '..\processing\processed_data\jsonls'
out_path = 'policy'
out_name = 'policy_all_300.jsonl'

protoss_units = ["COLOSSUS", "MOTHERSHIP", "NEXUS", "PYLON", "ASSIMILATOR", "GATEWAY", "FORGE", "FLEETBEACON", 
                 "TWILIGHTCOUNCIL", "PHOTONCANNON", "STARGATE", "TEMPLARARCHIVE", "DARKSHRINE", "ROBOTICSBAY",
                 "ROBOTICSFACILITY", "CYBERNETICSCORE", "ZEALOT", "STALKER", "HIGHTEMPLAR", "DARKTEMPLAR", 
                 "SENTRY", "PHOENIX", "CARRIER", "VOIDRAY", "WARPPRISM", "OBSERVER", "IMMORTAL", "PROBE", "INTERCEPTOR", 
                 "WARPGATE", "WARPPRISMPHASING", "ARCHON", "ADEPT", "MOTHERSHIPCORE", "ORACLE", "TEMPEST", "RESOURCEBLOCKER", 
                 "ICEPROTOSSCRATES", "PROTOSSCRATES", "DISRUPTOR", "VOIDMPIMMORTALREVIVECORPSE", "ORACLESTASISTRAP", 
                 "DISRUPTORPHASED", "RELEASEINTERCEPTORSBEACON", "ADEPTPHASESHIFT", "REPLICANT", "CORSAIRMP", 
                 "SCOUTMP", "ARBITERMP", "PYLONOVERCHARGED", "SHIELDBATTERY", "OBSERVERSIEGEMODE", "ASSIMILATORRICH"]

#Read jsonl file
def read_jsonl(file_path):
    with open(file_path, 'r') as file:
        return [json.loads(line) for line in file]
    
#List of all .jsonl files in inpath
jsonl_files = [file for file in os.listdir(in_path) if file.endswith('.jsonl')]

#Join all the data
combined_data = []
for file_name in jsonl_files:
    file_path = os.path.join(in_path, file_name)
    data = read_jsonl(file_path)
    combined_data.extend(data)

# def flatten_state(state):
#     flat_state = []
#     for key, value in state.items():
#         if isinstance(value, dict):
#             flat_state.extend(value.values())
#         else:
#             flat_state.append(value)
#     return tuple(flat_state)

#Flatten only my_units as the states
def flatten_state(state):
    flat_state = []
    my_units = state.get('my_units', {})
    flat_state.extend(my_units.values())
    return tuple(flat_state)

#Define all possible actions
all_actions = [entry['a'] for entry in combined_data]
unique_actions = list(set(all_actions))

#Initialize Q-table
q_table = defaultdict(lambda: defaultdict(float))

#Define learning parameters
alpha = 0.01;   #learning rate
gamma = 0.9;    #discount factor
epsilon = 0.3;  #exploration rate

#SARSA Learning Loop
for entry in combined_data:
    current_state = flatten_state(entry['s'])
    action = entry['a']
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

#Converting states back to original
# def reconstruct_state(flat_state):
#     num_unit_keys = len(protoss_units)

#     #split the flat states into parts
#     # enemy_units_values = flat_state[:num_unit_keys]
#     my_units_values = flat_state[:num_unit_keys]
#     # minerals, gas = flat_state[num_unit_keys*2], flat_state[num_unit_keys*2 + 1]

#     #Reconstruct the original state
#     original_state = dict(zip(protoss_units, my_units_values))
#     # original_state = {
#     #     "enemy_units": dict(zip(unit_keys, enemy_units_values)),
#     #     "my_units": dict(zip(unit_keys, my_units_values))
#     #     "minerals": minerals,
#     #     "gas": gas
#     # }

#     return original_state

#Create nested dict for the states in policy
def nest_states(old_policy):
    new_policy = {}
    for flat_state, action in old_policy.items():
        current_level = new_policy
        for key in flat_state[:-1]:
            if key not in current_level:
                current_level[key] = {}
            current_level = current_level[key]
        current_level[flat_state[-1]] = action
    return new_policy

policy = nest_states(policy)

#Write the policy to a .jsonl file
output_file_path = os.path.join(out_path, out_name)
with open(output_file_path, 'w') as file:
    json.dump(policy, file)

print(f"Policy file saved to {output_file_path}")