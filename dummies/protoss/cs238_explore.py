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

class CS238Explore(KnowledgeBot):
    def __init__(self):
        super().__init__("CS 238 Explore")
        self.action = None
        self.action_unit_count = 0
        self.queue_next_action = False
    
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

    async def execute(self):
        super().execute()

        # If we picked an action, check if we've done it yet, unless it's invalid
        new_action = False
        if self.queue_next_action:
            new_action = True
        elif self.action:
            if len(self.knowledge.unit_cache.own(self.action)) != self.action_unit_count or not self.is_action_valid(self.action):
                new_action = True
        else:
            new_action = True
        
        # Pick a new action
        if new_action:
            all_actions = [
                UnitTypeId.PROBE,
                UnitTypeId.ZEALOT, UnitTypeId.STALKER, UnitTypeId.SENTRY, UnitTypeId.ADEPT, UnitTypeId.HIGHTEMPLAR, UnitTypeId.DARKTEMPLAR, UnitTypeId.IMMORTAL, UnitTypeId.COLOSSUS, UnitTypeId.DISRUPTOR, UnitTypeId.OBSERVER, UnitTypeId.WARPPRISM, UnitTypeId.PHOENIX, UnitTypeId.VOIDRAY, UnitTypeId.ORACLE, UnitTypeId.CARRIER, UnitTypeId.TEMPEST,
                UnitTypeId.NEXUS, UnitTypeId.ASSIMILATOR,
                UnitTypeId.PYLON, UnitTypeId.GATEWAY, UnitTypeId.FORGE, UnitTypeId.CYBERNETICSCORE, UnitTypeId.PHOTONCANNON, UnitTypeId.SHIELDBATTERY, UnitTypeId.TWILIGHTCOUNCIL, UnitTypeId.STARGATE, UnitTypeId.ROBOTICSFACILITY, UnitTypeId.TEMPLARARCHIVE, UnitTypeId.DARKSHRINE, UnitTypeId.FLEETBEACON, UnitTypeId.ROBOTICSBAY,
            ]

            only_want_one = [UnitTypeId.FORGE, UnitTypeId.CYBERNETICSCORE, UnitTypeId.TWILIGHTCOUNCIL, UnitTypeId.TEMPLARARCHIVE, UnitTypeId.DARKSHRINE, UnitTypeId.FLEETBEACON]
            for action in only_want_one:
                if len(self.knowledge.unit_cache.own(action)):
                    all_actions.remove(action)
            
            valid_actions = [action for action in all_actions if self.is_action_valid(action)]
            self.action = random.choice(valid_actions) if len(valid_actions) > 0 else None
            self.action_unit_count = len(self.knowledge.unit_cache.own(self.action))
            self.queue_next_action = self.knowledge.can_afford(self.action, False)

            print(f"valid actions {valid_actions}")
            print(f"new action {self.action}")
        else:
            print(f"old action {self.action}")

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
