import numpy as np
import random
import json
from collections import defaultdict

#Load Jsonl data
with open('game5.jsonl', 'r') as file:
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

#Define all possible actions
all_actions = [entry['a'] for entry in data]
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
def reconstruct_state(flat_state):
    unit_keys = ["COLOSSUS", "MOTHERSHIP", "NEXUS", "PYLON", "ASSIMILATOR", "GATEWAY", "FORGE", "FLEETBEACON", 
                 "TWILIGHTCOUNCIL", "PHOTONCANNON", "STARGATE", "TEMPLARARCHIVE", "DARKSHRINE", "ROBOTICSBAY",
                 "ROBOTICSFACILITY", "CYBERNETICSCORE", "ZEALOT", "STALKER", "HIGHTEMPLAR", "DARKTEMPLAR", 
                 "SENTRY", "PHOENIX", "CARRIER", "VOIDRAY", "WARPPRISM", "OBSERVER", "IMMORTAL", "PROBE", "INTERCEPTOR", 
                 "WARPGATE", "WARPPRISMPHASING", "ARCHON", "ADEPT", "MOTHERSHIPCORE", "ORACLE", "TEMPEST", "RESOURCEBLOCKER", 
                 "ICEPROTOSSCRATES", "PROTOSSCRATES", "DISRUPTOR", "VOIDMPIMMORTALREVIVECORPSE", "ORACLESTASISTRAP", 
                 "DISRUPTORPHASED", "RELEASEINTERCEPTORSBEACON", "ADEPTPHASESHIFT", "REPLICANT", "CORSAIRMP", 
                 "SCOUTMP", "ARBITERMP", "PYLONOVERCHARGED", "SHIELDBATTERY", "OBSERVERSIEGEMODE", "ASSIMILATORRICH"]
    num_unit_keys = len(unit_keys)

    #split the flat states into parts
    enemy_units_values = flat_state[:num_unit_keys]
    my_units_values = flat_state[num_unit_keys : num_unit_keys*2]
    minerals, gas = flat_state[num_unit_keys*2], flat_state[num_unit_keys*2 + 1]

    #Reconstruct the original state
    original_state = {
        "enemy_units": dict(zip(unit_keys, enemy_units_values)),
        "my_units": dict(zip(unit_keys, my_units_values)),
        "minerals": minerals,
        "gas": gas
    }

    return original_state

#Write the policy to a .jsonl file
with open('policy_game5.jsonl', 'w') as file:
    for flat_state, action in policy.items():
        original_state = reconstruct_state(flat_state)

        policy_line = {"s":original_state, "a":action}
        json_line = json.dumps(policy_line)
        file.write(json_line + '\n')