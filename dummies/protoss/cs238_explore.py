from enum import Enum

from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId

from sharpy.knowledges import KnowledgeBot, Knowledge
from sharpy.plans import BuildOrder, Step, SequentialList, StepBuildGas
from sharpy.plans.acts import *
from sharpy.plans.acts.protoss import *
from sharpy.plans.require import *
from sharpy.plans.tactics import *

class ProxyCS238Explore(ActBase):
    class ActionEnum(Enum):
        TRAIN = 1
        BUILD = 2
        BUILD_EXPANSION = 3
        BUILD_GAS = 4

    def __init__(self):
        super().__init__()

    async def start(self, knowledge: Knowledge):
        await super().start(knowledge)

    async def execute(self) -> bool:
        print("exe")
        
        return False
    
    def determine_action(self):
        self.actionType = self.ActionEnum.TRAIN
        self.actionUnitTypeId = UnitTypeId.PROBE

class CS238Explore(KnowledgeBot):
    def __init__(self):
        super().__init__("CS 238 Explore")
    
    async def create_plan(self) -> BuildOrder:
        return BuildOrder(
            Step(None, ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS)),
            Step(None, ProxyCS238Explore()),
            SequentialList(
                MineOpenBlockedBase(),
                PlanZoneDefense(),
                RestorePower(),
                DistributeWorkers(),
                Step(None, SpeedMining(), lambda ai: ai.client.game_step > 5),
                PlanZoneGather(),
                Step(None, PlanZoneAttack(4)),
                PlanFinishEnemy(),
            )
        )


class LadderBot(CS238Explore):
    @property
    def my_race(self):
        return Race.Protoss
