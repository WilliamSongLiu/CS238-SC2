from math import floor
from typing import List, Optional

from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.position import Point2
from sc2.unit import Unit

from sharpy.knowledges import KnowledgeBot, Knowledge
from sharpy.managers.core import ManagerBase
from sharpy.managers.core.building_solver import WallType
from sharpy.managers.core.roles import UnitTask
from sharpy.plans import BuildOrder, Step, SequentialList, StepBuildGas
from sharpy.plans.acts import *
from sharpy.plans.acts.protoss import *
from sharpy.plans.require import *
from sharpy.plans.tactics import *
from sharpy.utils import select_build_index

class ProxyCS238Explore(ActBase):
    def __init__(self):
        super().__init__()
        self.proxy_worker_tag: Optional[int] = None
        self.proxy_worker_tag2: Optional[int] = None

    async def start(self, knowledge: Knowledge):
        await super().start(knowledge)
        self.enemy_main: Point2 = self.zone_manager.expansion_zones[-1].center_location
        self.natural: Point2 = self.zone_manager.expansion_zones[-2].center_location

        self.enemy_ramp = self.zone_manager.enemy_expansion_zones[0].ramp
        d = self.enemy_main.distance_to(self.natural)
        height = self.ai.get_terrain_height(self.natural)
        self.between = self.natural.towards(self.enemy_main, 5)

        for i in range(4, floor(d)):
            pos = self.natural.towards(self.enemy_main, i + 2).rounded
            if height == self.ai.get_terrain_height(pos):
                self.between = pos

        self.pylons: List[Point2] = [
            self.natural,
            self.enemy_ramp.bottom_center.towards(self.between, 2).towards(self.natural, 1),
            self.enemy_ramp.top_center.towards(self.enemy_main, 4),
        ]

        if knowledge.enemy_race != Race.Zerg:
            self.pylons.append(self.between.towards(self.enemy_main, 6))
            self.pylons.append(self.enemy_ramp.top_center.towards(self.enemy_main, 8))
            self.pylons.append(self.enemy_main.towards(self.enemy_ramp.top_center, 4))
        else:
            self.pylons.append(self.enemy_main.towards(self.enemy_ramp.top_center, 10))

    async def execute(self) -> bool:
        worker = self.get_worker()
        cannon_worker = self.get_cannon_worker()
        if not worker and not cannon_worker:
            return True

        if cannon_worker:
            await self.micro_cannon_worker(cannon_worker)
        if worker:
            await self.micro_pylon_worker(worker)
        return False

class CS238Explore(KnowledgeBot):
    def __init__(self):
        super().__init__("CS 238 Explore")

    async def create_plan(self) -> BuildOrder:
        return BuildOrder(
            Step(
                None,
                ChronoUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS),
                skip=UnitExists(UnitTypeId.PROBE, 40, include_pending=True),
                skip_until=UnitExists(UnitTypeId.ASSIMILATOR, 1),
            ),
            SequentialList(
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 14),
                GridBuilding(UnitTypeId.PYLON, 1),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 16),
                BuildGas(1),
                GridBuilding(UnitTypeId.GATEWAY, 1),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 20),
                Expand(2),
                GridBuilding(UnitTypeId.CYBERNETICSCORE, 1),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 21),
                BuildGas(2),
                ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 22),
                GridBuilding(UnitTypeId.PYLON, 1),
                BuildOrder(
                    AutoPylon(),
                    Tech(UpgradeId.WARPGATERESEARCH),
                    [
                        ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 22),
                        Step(UnitExists(UnitTypeId.NEXUS, 2), ActUnit(UnitTypeId.PROBE, UnitTypeId.NEXUS, 44)),
                        StepBuildGas(3, skip=Gas(300)),
                    ],
                    [ProtossUnit(UnitTypeId.STALKER, 100)],
                    [GridBuilding(UnitTypeId.GATEWAY, 7), StepBuildGas(4, skip=Gas(200))],
                ),
            ),
            SequentialList(
                MineOpenBlockedBase(),
                PlanZoneDefense(),
                RestorePower(),
                DistributeWorkers(),
                Step(None, SpeedMining(), lambda ai: ai.client.game_step > 5),
                PlanZoneGather(),
                Step(UnitReady(UnitTypeId.GATEWAY, 4), PlanZoneAttack(4)),
                PlanFinishEnemy(),
            ),
        )


class LadderBot(CS238Explore):
    @property
    def my_race(self):
        return Race.Protoss
