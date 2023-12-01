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
    class ActionEnum(Enum):
        TRAIN = 1
        TRAIN_PROBE = 2
        BUILD = 10
        BUILD_EXPANSION = 11
        BUILD_GAS = 12
    
    def __init__(self):
        super().__init__("CS 238 Explore")
    
    # This breaks everything
    # async def on_start(self):
    #     super().on_start()
    
    async def execute(self):
        print("b")
        super().execute()
        self.actionType = self.ActionEnum.TRAIN_PROBE
        self.actionUnitTypeId = UnitTypeId.PROBE

    def actions(self) -> ActBase:
        return [
            
        ]

    async def create_plan(self) -> BuildOrder:
        print("a")
        return BuildOrder(
            Step(lambda k: self.actionType == self.ActionEnum.TRAIN_PROBE, ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS)),
            Step(lambda k: self.actionType == self.ActionEnum.TRAIN, ProtossUnit(self.actionUnitTypeId)),
            Step(lambda k: self.actionType == self.ActionEnum.BUILD, GridBuilding(self.actionUnitTypeId, 9999)),
            Step(lambda k: self.actionType == self.ActionEnum.BUILD_EXPANSION, Expand(9999)),
            Step(lambda k: self.actionType == self.ActionEnum.BUILD_GAS, BuildGas(9999)),

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
