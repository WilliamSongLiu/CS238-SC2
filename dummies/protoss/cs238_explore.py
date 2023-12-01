from enum import Enum

from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId

from sharpy.knowledges import KnowledgeBot, Knowledge
from sharpy.plans import BuildOrder, Step, SequentialList, StepBuildGas
from sharpy.plans.acts import *
from sharpy.plans.acts.protoss import *
from sharpy.plans.require import *
from sharpy.plans.tactics import *

class CS238Explore(KnowledgeBot):
    def __init__(self):
        super().__init__("CS 238 Explore")
        self.actionUnitTypeId = UnitTypeId.PROBE
    
    # This breaks everything
    # async def on_start(self):
    #     pass
    
    async def execute(self):
        super().execute()
        self.actionUnitTypeId = UnitTypeId.PROBE

    def train_actions(self):
        return (
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ZEALOT, ProtossUnit(UnitTypeId.ZEALOT)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.STALKER, ProtossUnit(UnitTypeId.STALKER)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.SENTRY, ProtossUnit(UnitTypeId.SENTRY)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ADEPT, ProtossUnit(UnitTypeId.ADEPT)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.HIGHTEMPLAR, ProtossUnit(UnitTypeId.HIGHTEMPLAR)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.DARKTEMPLAR, ProtossUnit(UnitTypeId.DARKTEMPLAR)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.IMMORTAL, ProtossUnit(UnitTypeId.IMMORTAL)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.COLOSSUS, ProtossUnit(UnitTypeId.COLOSSUS)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.DISRUPTOR, ProtossUnit(UnitTypeId.DISRUPTOR)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.OBSERVER, ProtossUnit(UnitTypeId.OBSERVER)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.WARPPRISM, ProtossUnit(UnitTypeId.WARPPRISM)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.PHOENIX, ProtossUnit(UnitTypeId.PHOENIX)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.VOIDRAY, ProtossUnit(UnitTypeId.VOIDRAY)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ORACLE, ProtossUnit(UnitTypeId.ORACLE)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.CARRIER, ProtossUnit(UnitTypeId.CARRIER)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.TEMPEST, ProtossUnit(UnitTypeId.TEMPEST)),
        )
    
    def build_actions(self):
        return (
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.PYLON, GridBuilding(UnitTypeId.PYLON, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.GATEWAY, GridBuilding(UnitTypeId.GATEWAY, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.FORGE, GridBuilding(UnitTypeId.FORGE, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.CYBERNETICSCORE, GridBuilding(UnitTypeId.CYBERNETICSCORE, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.PHOTONCANNON, GridBuilding(UnitTypeId.PHOTONCANNON, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.SHIELDBATTERY, GridBuilding(UnitTypeId.SHIELDBATTERY, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.TWILIGHTCOUNCIL, GridBuilding(UnitTypeId.TWILIGHTCOUNCIL, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.STARGATE, GridBuilding(UnitTypeId.STARGATE, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ROBOTICSFACILITY, GridBuilding(UnitTypeId.ROBOTICSFACILITY, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.TEMPLARARCHIVE, GridBuilding(UnitTypeId.TEMPLARARCHIVE, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.DARKSHRINE, GridBuilding(UnitTypeId.DARKSHRINE, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.FLEETBEACON, GridBuilding(UnitTypeId.FLEETBEACON, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ROBOTICSBAY, GridBuilding(UnitTypeId.ROBOTICSBAY, 9999)),
        )

    async def create_plan(self) -> BuildOrder:
        print("create_plan")
        return BuildOrder(
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.PROBE, ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS)),
            *self.train_actions(),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.NEXUS, Expand(9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ASSIMILATOR, BuildGas(9999)),
            *self.build_actions(),

            ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS),
            SequentialList(
                MineOpenBlockedBase(),
                PlanZoneDefense(),
                RestorePower(),
                DistributeWorkers(),
                Step(None, SpeedMining(), lambda ai: ai.client.game_step > 5),
                PlanZoneGather(),
                PlanZoneAttack(4),
                PlanFinishEnemy(),
            )
        )


class LadderBot(CS238Explore):
    @property
    def my_race(self):
        return Race.Protoss
