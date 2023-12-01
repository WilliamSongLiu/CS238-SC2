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
    
    # This breaks everything
    # async def on_start(self):
    #     super().on_start()
    
    async def execute(self):
        print("b")
        super().execute()
        self.actionUnitTypeId = UnitTypeId.PROBE

    def train_actions(self):
        return (
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.COLOSSUS, ProtossUnit(UnitTypeId.COLOSSUS)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.MOTHERSHIP, ProtossUnit(UnitTypeId.MOTHERSHIP)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.NEXUS, ProtossUnit(UnitTypeId.NEXUS)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.PYLON, ProtossUnit(UnitTypeId.PYLON)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ASSIMILATOR, ProtossUnit(UnitTypeId.ASSIMILATOR)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.GATEWAY, ProtossUnit(UnitTypeId.GATEWAY)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.FORGE, ProtossUnit(UnitTypeId.FORGE)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.FLEETBEACON, ProtossUnit(UnitTypeId.FLEETBEACON)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.TWILIGHTCOUNCIL, ProtossUnit(UnitTypeId.TWILIGHTCOUNCIL)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.PHOTONCANNON, ProtossUnit(UnitTypeId.PHOTONCANNON)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.STARGATE, ProtossUnit(UnitTypeId.STARGATE)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.TEMPLARARCHIVE, ProtossUnit(UnitTypeId.TEMPLARARCHIVE)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.DARKSHRINE, ProtossUnit(UnitTypeId.DARKSHRINE)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ROBOTICSBAY, ProtossUnit(UnitTypeId.ROBOTICSBAY)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ROBOTICSFACILITY, ProtossUnit(UnitTypeId.ROBOTICSFACILITY)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.CYBERNETICSCORE, ProtossUnit(UnitTypeId.CYBERNETICSCORE)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ZEALOT, ProtossUnit(UnitTypeId.ZEALOT)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.STALKER, ProtossUnit(UnitTypeId.STALKER)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.HIGHTEMPLAR, ProtossUnit(UnitTypeId.HIGHTEMPLAR)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.DARKTEMPLAR, ProtossUnit(UnitTypeId.DARKTEMPLAR)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.SENTRY, ProtossUnit(UnitTypeId.SENTRY)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.PHOENIX, ProtossUnit(UnitTypeId.PHOENIX)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.CARRIER, ProtossUnit(UnitTypeId.CARRIER)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.VOIDRAY, ProtossUnit(UnitTypeId.VOIDRAY)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.WARPPRISM, ProtossUnit(UnitTypeId.WARPPRISM)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.OBSERVER, ProtossUnit(UnitTypeId.OBSERVER)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.IMMORTAL, ProtossUnit(UnitTypeId.IMMORTAL)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.INTERCEPTOR, ProtossUnit(UnitTypeId.INTERCEPTOR)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.WARPGATE, ProtossUnit(UnitTypeId.WARPGATE)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.WARPPRISMPHASING, ProtossUnit(UnitTypeId.WARPPRISMPHASING)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ARCHON, ProtossUnit(UnitTypeId.ARCHON)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ADEPT, ProtossUnit(UnitTypeId.ADEPT)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.MOTHERSHIPCORE, ProtossUnit(UnitTypeId.MOTHERSHIPCORE)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ORACLE, ProtossUnit(UnitTypeId.ORACLE)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.TEMPEST, ProtossUnit(UnitTypeId.TEMPEST)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.RESOURCEBLOCKER, ProtossUnit(UnitTypeId.RESOURCEBLOCKER)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ICEPROTOSSCRATES, ProtossUnit(UnitTypeId.ICEPROTOSSCRATES)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.PROTOSSCRATES, ProtossUnit(UnitTypeId.PROTOSSCRATES)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.DISRUPTOR, ProtossUnit(UnitTypeId.DISRUPTOR)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.VOIDMPIMMORTALREVIVECORPSE, ProtossUnit(UnitTypeId.VOIDMPIMMORTALREVIVECORPSE)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ORACLESTASISTRAP, ProtossUnit(UnitTypeId.ORACLESTASISTRAP)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.DISRUPTORPHASED, ProtossUnit(UnitTypeId.DISRUPTORPHASED)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.RELEASEINTERCEPTORSBEACON, ProtossUnit(UnitTypeId.RELEASEINTERCEPTORSBEACON)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ADEPTPHASESHIFT, ProtossUnit(UnitTypeId.ADEPTPHASESHIFT)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.REPLICANT, ProtossUnit(UnitTypeId.REPLICANT)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.CORSAIRMP, ProtossUnit(UnitTypeId.CORSAIRMP)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.SCOUTMP, ProtossUnit(UnitTypeId.SCOUTMP)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ARBITERMP, ProtossUnit(UnitTypeId.ARBITERMP)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.PYLONOVERCHARGED, ProtossUnit(UnitTypeId.PYLONOVERCHARGED)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.SHIELDBATTERY, ProtossUnit(UnitTypeId.SHIELDBATTERY)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.OBSERVERSIEGEMODE, ProtossUnit(UnitTypeId.OBSERVERSIEGEMODE)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ASSIMILATORRICH, ProtossUnit(UnitTypeId.ASSIMILATORRICH)),
        )

    async def create_plan(self) -> BuildOrder:
        print("a")
        return BuildOrder(
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.PROBE, ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS)),
            *self.train_actions(),
            # Step(lambda k: self.actionUnitTypeId == self.ActionEnum.BUILD, GridBuilding(self.actionUnitTypeId, 9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.NEXUS, Expand(9999)),
            Step(lambda k: self.actionUnitTypeId == UnitTypeId.ASSIMILATOR, BuildGas(9999)),

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
