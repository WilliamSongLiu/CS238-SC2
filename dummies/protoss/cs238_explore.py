from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.dicts.unit_trained_from import UNIT_TRAINED_FROM
from sc2.dicts.unit_train_build_abilities import TRAIN_INFO

from sharpy.knowledges import KnowledgeBot
from sharpy.plans import BuildOrder, Step, SequentialList
from sharpy.plans.acts import *
from sharpy.plans.acts.protoss import *
from sharpy.plans.require import *
from sharpy.plans.tactics import *

import random
import json

class CS238Explore(KnowledgeBot):
    def __init__(self):
        super().__init__("CS 238 Explore")
        self.action = None
        self.action_unit_count = 0
        self.action_wanted_turns = 0
    
    # This breaks everything
    # async def on_start(self):
    #     pass
    
    def is_action_valid(self, action):
        if action not in UNIT_TRAINED_FROM:
            return False
        for unit_from in UNIT_TRAINED_FROM[action]:
            if len(self.knowledge.unit_cache.own(unit_from)) == 0:
                continue
            entry = None
            if action in TRAIN_INFO[unit_from]:
                entry = TRAIN_INFO[unit_from][action]
            elif action in TRAIN_INFO[unit_from][UnitTypeId.PROBE]:
                entry = TRAIN_INFO[unit_from][UnitTypeId.PROBE][action]
            if not entry:
                continue
            if "required_building" not in entry or len(self.knowledge.unit_cache.own(entry["required_building"])) > 0:
                return True
        return False
    
    def random_policy(self):
        # If we picked an action, check if we've done it yet, unless it's invalid, or if we can afford it meaning we can start the next one too, or if we've wanted it for too long
        self.action_wanted_turns += 1
        new_action = False
        if self.action:
            if len(self.knowledge.unit_cache.own(self.action)) != self.action_unit_count or not self.is_action_valid(self.action) or self.knowledge.can_afford(self.action, check_supply_cost=False) or self.action_wanted_turns >= 50:
                new_action = True
        else:
            new_action = True
        
        # Pick a new action
        if new_action:
            train_actions = [UnitTypeId.ZEALOT, UnitTypeId.STALKER, UnitTypeId.SENTRY, UnitTypeId.ADEPT, UnitTypeId.HIGHTEMPLAR, UnitTypeId.DARKTEMPLAR, UnitTypeId.IMMORTAL, UnitTypeId.COLOSSUS, UnitTypeId.DISRUPTOR, UnitTypeId.OBSERVER, UnitTypeId.WARPPRISM, UnitTypeId.PHOENIX, UnitTypeId.VOIDRAY, UnitTypeId.ORACLE, UnitTypeId.CARRIER, UnitTypeId.TEMPEST]
            build_actions = [UnitTypeId.GATEWAY, UnitTypeId.FORGE, UnitTypeId.CYBERNETICSCORE, UnitTypeId.PHOTONCANNON, UnitTypeId.TWILIGHTCOUNCIL, UnitTypeId.STARGATE, UnitTypeId.ROBOTICSFACILITY, UnitTypeId.TEMPLARARCHIVE, UnitTypeId.DARKSHRINE, UnitTypeId.FLEETBEACON, UnitTypeId.ROBOTICSBAY]
            all_actions = [
                UnitTypeId.PROBE,
                *train_actions,
                UnitTypeId.NEXUS, UnitTypeId.ASSIMILATOR, UnitTypeId.PYLON,
                *build_actions
            ]

            only_want_one = [UnitTypeId.FORGE, UnitTypeId.CYBERNETICSCORE, UnitTypeId.TWILIGHTCOUNCIL, UnitTypeId.TEMPLARARCHIVE, UnitTypeId.DARKSHRINE, UnitTypeId.FLEETBEACON, UnitTypeId.ROBOTICSBAY]
            for action in only_want_one:
                if len(self.knowledge.unit_cache.own(action)):
                    all_actions.remove(action)
            
            valid_actions = [action for action in all_actions if self.is_action_valid(action)]
            valid_action_weights = [1 for action in valid_actions]
            for i in range(len(valid_actions)):
                if valid_actions[i] == UnitTypeId.PROBE:
                    valid_action_weights[i] = 20 if len(self.knowledge.unit_cache.own(UnitTypeId.PROBE)) < len(self.knowledge.unit_cache.own(UnitTypeId.NEXUS)) * 18 else 0
                elif valid_actions[i] == UnitTypeId.NEXUS:
                    valid_action_weights[i] = 5 if len(self.knowledge.unit_cache.own(UnitTypeId.PROBE)) >= len(self.knowledge.unit_cache.own(UnitTypeId.NEXUS)) * 14 else 0
                elif valid_actions[i] == UnitTypeId.ASSIMILATOR:
                    valid_action_weights[i] = 10 if len(self.knowledge.unit_cache.own(UnitTypeId.ASSIMILATOR)) < len(self.knowledge.unit_cache.own(UnitTypeId.NEXUS)) * 2 and self.vespene < 300 else 0
                elif valid_actions[i] == UnitTypeId.PYLON:
                    if self.supply_left < 3:
                        valid_action_weights[i] = 10
                    elif self.supply_left < 10:
                        valid_action_weights[i] = 5
                    else:
                        valid_action_weights[i] = 1
                elif valid_actions[i] in train_actions:
                    valid_action_weights[i] = 5 if self.supply_left >= 10 else 3
                elif valid_actions[i] in build_actions:
                    valid_action_weights[i] = 3 if self.supply_left < 10 else 1

            self.action = random.choices(valid_actions, valid_action_weights, k=1)[0] if len(valid_actions) > 0 else None
            self.action_unit_count = len(self.knowledge.unit_cache.own(self.action)) if self.action else 0
            self.action_wanted_turns = 0

        #     print(f"valid actions {valid_actions}")
        #     print(f"new action {self.action}")
        # else:
        #     print(f"old action {self.action}")
    
    def trained_policy(self):
        def load_policy(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        
        def get_state():
            protoss_units = ['COLOSSUS', 'MOTHERSHIP', 'NEXUS', 'PYLON', 'ASSIMILATOR', 'GATEWAY', 'FORGE', 'FLEETBEACON', 'TWILIGHTCOUNCIL', 'PHOTONCANNON', 'STARGATE', 'TEMPLARARCHIVE', 'DARKSHRINE', 'ROBOTICSBAY', 'ROBOTICSFACILITY', 'CYBERNETICSCORE', 'ZEALOT', 'STALKER', 'HIGHTEMPLAR', 'DARKTEMPLAR', 'SENTRY', 'PHOENIX', 'CARRIER', 'VOIDRAY', 'WARPPRISM', 'OBSERVER', 'IMMORTAL', 'PROBE', 'INTERCEPTOR', 'WARPGATE', 'WARPPRISMPHASING', 'ARCHON', 'ADEPT', 'MOTHERSHIPCORE', 'ORACLE', 'TEMPEST', 'RESOURCEBLOCKER', 'ICEPROTOSSCRATES', 'PROTOSSCRATES', 'DISRUPTOR', 'VOIDMPIMMORTALREVIVECORPSE', 'ORACLESTASISTRAP', 'DISRUPTORPHASED', 'RELEASEINTERCEPTORSBEACON', 'ADEPTPHASESHIFT', 'REPLICANT', 'CORSAIRMP', 'SCOUTMP', 'ARBITERMP', 'PYLONOVERCHARGED', 'SHIELDBATTERY', 'OBSERVERSIEGEMODE', 'ASSIMILATORRICH']
            my_units = self.unit_cache.get_my_units()
            my_units_caps = {}
            for key, value in my_units.items():
                my_units_caps[key.upper()] = value
            return tuple(["0" if unit not in my_units_caps else str(my_units_caps[unit]) for unit in protoss_units])

        def get_action(policy, state):
            current_level = policy
            for key in state:
                if key in current_level:
                    current_level = current_level[key]
                else:
                    return None
            return current_level

        policy = load_policy(r"SARSA\policy\policy_2.jsonl")
        state = get_state()
        action = get_action(policy, state)
        if action:
            print("Found state in policy")
            self.action = action
        else:
            print("State not found, resorting to random")
            self.random_policy()
    
    async def execute(self):
        super().execute()
        self.trained_policy()

    def train_actions(self):
        return (
            Step(lambda k: self.action == UnitTypeId.ZEALOT, ProtossUnit(UnitTypeId.ZEALOT)),
            Step(lambda k: self.action == UnitTypeId.STALKER, ProtossUnit(UnitTypeId.STALKER)),
            Step(lambda k: self.action == UnitTypeId.SENTRY, ProtossUnit(UnitTypeId.SENTRY)),
            Step(lambda k: self.action == UnitTypeId.ADEPT, ProtossUnit(UnitTypeId.ADEPT)),
            Step(lambda k: self.action == UnitTypeId.HIGHTEMPLAR, ProtossUnit(UnitTypeId.HIGHTEMPLAR)),
            Step(lambda k: self.action == UnitTypeId.DARKTEMPLAR, ProtossUnit(UnitTypeId.DARKTEMPLAR)),
            Step(lambda k: self.action == UnitTypeId.IMMORTAL, ProtossUnit(UnitTypeId.IMMORTAL)),
            Step(lambda k: self.action == UnitTypeId.COLOSSUS, ProtossUnit(UnitTypeId.COLOSSUS)),
            Step(lambda k: self.action == UnitTypeId.DISRUPTOR, ProtossUnit(UnitTypeId.DISRUPTOR)),
            Step(lambda k: self.action == UnitTypeId.OBSERVER, ProtossUnit(UnitTypeId.OBSERVER)),
            Step(lambda k: self.action == UnitTypeId.WARPPRISM, ProtossUnit(UnitTypeId.WARPPRISM)),
            Step(lambda k: self.action == UnitTypeId.PHOENIX, ProtossUnit(UnitTypeId.PHOENIX)),
            Step(lambda k: self.action == UnitTypeId.VOIDRAY, ProtossUnit(UnitTypeId.VOIDRAY)),
            Step(lambda k: self.action == UnitTypeId.ORACLE, ProtossUnit(UnitTypeId.ORACLE)),
            Step(lambda k: self.action == UnitTypeId.CARRIER, ProtossUnit(UnitTypeId.CARRIER)),
            Step(lambda k: self.action == UnitTypeId.TEMPEST, ProtossUnit(UnitTypeId.TEMPEST)),
        )
    
    def build_actions(self):
        return (
            Step(lambda k: self.action == UnitTypeId.PYLON, GridBuilding(UnitTypeId.PYLON, 9999)),
            Step(lambda k: self.action == UnitTypeId.GATEWAY, GridBuilding(UnitTypeId.GATEWAY, 9999)),
            Step(lambda k: self.action == UnitTypeId.FORGE, GridBuilding(UnitTypeId.FORGE, 9999)),
            Step(lambda k: self.action == UnitTypeId.CYBERNETICSCORE, GridBuilding(UnitTypeId.CYBERNETICSCORE, 9999)),
            Step(lambda k: self.action == UnitTypeId.PHOTONCANNON, GridBuilding(UnitTypeId.PHOTONCANNON, 9999)),
            Step(lambda k: self.action == UnitTypeId.SHIELDBATTERY, GridBuilding(UnitTypeId.SHIELDBATTERY, 9999)),
            Step(lambda k: self.action == UnitTypeId.TWILIGHTCOUNCIL, GridBuilding(UnitTypeId.TWILIGHTCOUNCIL, 9999)),
            Step(lambda k: self.action == UnitTypeId.STARGATE, GridBuilding(UnitTypeId.STARGATE, 9999)),
            Step(lambda k: self.action == UnitTypeId.ROBOTICSFACILITY, GridBuilding(UnitTypeId.ROBOTICSFACILITY, 9999)),
            Step(lambda k: self.action == UnitTypeId.TEMPLARARCHIVE, GridBuilding(UnitTypeId.TEMPLARARCHIVE, 9999)),
            Step(lambda k: self.action == UnitTypeId.DARKSHRINE, GridBuilding(UnitTypeId.DARKSHRINE, 9999)),
            Step(lambda k: self.action == UnitTypeId.FLEETBEACON, GridBuilding(UnitTypeId.FLEETBEACON, 9999)),
            Step(lambda k: self.action == UnitTypeId.ROBOTICSBAY, GridBuilding(UnitTypeId.ROBOTICSBAY, 9999)),
        )

    async def create_plan(self) -> BuildOrder:
        print("create_plan")
        return BuildOrder(
            Step(lambda k: self.action == UnitTypeId.PROBE, ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS)),
            *self.train_actions(),
            Step(lambda k: self.action == UnitTypeId.NEXUS, Expand(9999)),
            Step(lambda k: self.action == UnitTypeId.ASSIMILATOR, BuildGas(9999)),
            *self.build_actions(),

            ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS),
            SequentialList(
                MineOpenBlockedBase(),
                PlanZoneDefense(),
                RestorePower(),
                DistributeWorkers(),
                Step(None, SpeedMining(), lambda ai: ai.client.game_step > 5),
                PlanZoneGather(),
                PlanZoneAttack(20),
                PlanFinishEnemy(),
            )
        )


class LadderBot(CS238Explore):
    @property
    def my_race(self):
        return Race.Protoss
