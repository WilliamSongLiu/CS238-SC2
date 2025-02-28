from typing import Dict, Set, List, KeysView

from sc2.data import Result
from sharpy.events import UnitDestroyedEvent
from sharpy.interfaces import IEnemyUnitsManager
from sharpy.managers.core.manager_base import ManagerBase
from sharpy.unit_count import UnitCount
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.unit import Unit

from sharpy.general.extended_power import ExtendedPower
from sharpy.managers.core.unit_value import UnitValue, REVERSE_MORPHS_DICT


class EnemyUnitsManager(ManagerBase, IEnemyUnitsManager):
    """Keeps track of enemy units and structures.

        Note that the class has many limitations, it does not account that
        * banelings are created by sacrificing zerglings
        * an archon is created by sacrificing two templars (dark templar or high templar).
        * orbital commands are transformed from command centers.
        * warp gates are transformed from gateways.
        *
        """

    unit_values: UnitValue

    def __init__(self):
        super().__init__()

        # Dictionary for enemy units. Key is unit type, values are sets of unit tags.
        self._known_enemy_units_dict: Dict[UnitTypeId, Set[int]] = {}
        # This is the count we have seen that are morphed from this base type
        self._morphed_type: Dict[UnitTypeId, int] = {}
        self._enemy_cloak_trigger = False

    async def start(self, knowledge: "Knowledge"):
        await super().start(knowledge)
        self.unit_values = knowledge.unit_values
        knowledge.register_on_unit_destroyed_listener(self.on_unit_destroyed)

    @property
    def unit_types(self) -> KeysView[UnitTypeId]:
        """Returns all unit types that we have seen the enemy to use."""
        return self._known_enemy_units_dict.keys()

    @property
    def enemy_worker_count(self) -> int:
        """Returns the amount of workers we know the enemy has"""
        worker_type = self.unit_values.enemy_worker_type
        return self.unit_count(worker_type)

    @property
    def enemy_composition(self) -> List[UnitCount]:
        lst: List[UnitCount] = []
        for unit_type in self._known_enemy_units_dict:
            unit_count = self.unit_count(unit_type)

            if unit_count > 0:
                lst.append(UnitCount(unit_type, unit_count))

        return lst

    def unit_count(self, unit_type: UnitTypeId) -> int:
        """Returns how many units enemy currently has of that unit type."""
        real_type = self.unit_values.real_type(unit_type)
        unit_tags = self._known_enemy_units_dict.get(real_type, set())
        return len(unit_tags) - self._morphed_type.get(real_type, 0)

    @property
    def enemy_total_power(self) -> ExtendedPower:
        """Returns the total power of all enemy units we currently know about.
         Assumes they are all in full health. Ignores workers and overlords."""
        total_power = ExtendedPower(self.unit_values)
        for type_id in self._known_enemy_units_dict:
            if self.unit_values.is_worker(type_id):
                continue

            if type_id == UnitTypeId.OVERLORD:
                continue

            count_for_unit_type = self.unit_count(type_id)
            total_power.add_unit(type_id, count_for_unit_type)

        return total_power

    async def update(self):
        self.cloak_check()
        types_check = set()

        for unit in self.ai.all_enemy_units:  # type: Unit
            real_type = self.unit_values.real_type(unit.type_id)

            if real_type not in types_check:
                types_check.add(real_type)

            # Ignore some units that are eg. temporary
            if real_type in ignored_types:
                continue

            if unit.is_snapshot:
                # Ignore snapshots aa they have a different tag than the "real" unit.
                continue

            if unit.is_hallucination:
                continue

            known_units = self._known_enemy_units_dict.setdefault(real_type, set())
            if unit.tag not in known_units:
                known_units.add(unit.tag)
                morphed_from = REVERSE_MORPHS_DICT.get(real_type, None)
                if morphed_from:
                    self._morphed_type[morphed_from] = self._morphed_type.get(morphed_from, 0) + 1
                self.print(f"Enemy unit {unit.tag} of type {real_type} discovered.")

        self.re_adjust_morphs(types_check)

        # enemy_tally = {}
        # for unit in self.ai.all_enemy_units:
        #     if unit.name not in enemy_tally:
        #         enemy_tally[unit.name] = 0
        #     enemy_tally[unit.name] += 1
        # enemy_tally = dict(sorted(enemy_tally.items()))
        # print(f"ENEMY_UNITS: {enemy_tally}")

    @property
    def enemy_cloak_trigger(self):
        return self._enemy_cloak_trigger

    def cloak_check(self):
        if self._enemy_cloak_trigger:
            return

        # Protoss cloaked units (observer can't attack)
        if self.unit_count(UnitTypeId.DARKTEMPLAR) > 0 or self.ai.enemy_structures(UnitTypeId.DARKSHRINE).exists:
            self._enemy_cloak_trigger = True

        if self.unit_count(UnitTypeId.MOTHERSHIP) > 0:
            self._enemy_cloak_trigger = True

        # Terran cloaked units
        if self.unit_count(UnitTypeId.BANSHEE) > 0:
            self._enemy_cloak_trigger = True

        if self.unit_count(UnitTypeId.WIDOWMINE) > 0:
            self._enemy_cloak_trigger = True

        if self.unit_count(UnitTypeId.GHOST) > 0 or self.ai.enemy_structures(UnitTypeId.GHOSTACADEMY):
            self._enemy_cloak_trigger = True

        # Zerg burrow
        if len(self.cache.enemy(UnitTypeId.ZERGLINGBURROWED)) > 0:
            self._enemy_cloak_trigger = True

        if len(self.cache.enemy(UnitTypeId.BANELINGBURROWED)) > 0:
            self._enemy_cloak_trigger = True

        if len(self.cache.enemy(UnitTypeId.ROACHBURROWED)) > 0:
            self._enemy_cloak_trigger = True

        if len(self.cache.enemy(UnitTypeId.RAVAGERBURROWED)) > 0:
            self._enemy_cloak_trigger = True

        if (
            self.unit_count(UnitTypeId.LURKER) > 0
            or self.ai.enemy_structures.of_type([UnitTypeId.LURKERDENMP, UnitTypeId.LURKERDEN]).exists
        ):
            self._enemy_cloak_trigger = True

    def danger_value(self, danger_for_unit: Unit, position: Point2) -> float:
        danger = 0
        for unit in self.ai.all_enemy_units:
            if not unit.is_ready:
                continue
            real_range = self.unit_values.real_range(unit, danger_for_unit)

            if real_range < 1:
                continue
            if danger_for_unit.is_flying:
                local_danger = unit.air_dps
            else:
                local_danger = unit.ground_dps

            distance = unit.distance_to(position)
            if distance < real_range:
                danger += local_danger + (1 - distance / real_range) * local_danger
            elif self.unit_values.real_speed(danger_for_unit) > self.unit_values.real_speed(unit):
                danger += max(0, (1.5 - distance / real_range) * local_danger)
            else:
                danger += max(0, (2 - distance / real_range) * local_danger)

        return danger

    def on_unit_destroyed(self, event: UnitDestroyedEvent):
        unit = event.unit
        if not unit or not unit.is_enemy:
            # We only care about enemy units here.
            return

        real_type = self.unit_values.real_type(unit.type_id)
        known_units = self._known_enemy_units_dict.get(real_type, set())

        if unit.tag in known_units:
            known_units.remove(unit.tag)

        self.print(f"Enemy unit {unit.tag} of type {real_type} died.")

    def print_contents(self):
        self.print("Contents:")
        for unit_type in self._known_enemy_units_dict:
            count = self.unit_count(unit_type)
            self.print(f"{unit_type} - {count}")

    async def on_end(self, game_result: Result):
        self.print_contents()

    async def post_update(self):
        pass

    def re_adjust_morphs(self, types_check: Set[UnitTypeId]):
        for type_id in types_check:
            count = len(self.cache.enemy(type_id))
            tags_count = len(self._known_enemy_units_dict.get(type_id, []))
            if count > tags_count - self._morphed_type.get(type_id, 0):
                self._morphed_type[type_id] = max(0, count - tags_count)


ignored_types: Set[UnitTypeId] = {
    # Zerg
    UnitTypeId.EGG,
    UnitTypeId.LARVA,
    UnitTypeId.INFESTORTERRAN,
    UnitTypeId.INFESTEDTERRANSEGG,
    UnitTypeId.CHANGELING,
    UnitTypeId.CHANGELINGMARINE,
    UnitTypeId.CHANGELINGMARINESHIELD,
    UnitTypeId.CHANGELINGZEALOT,
    UnitTypeId.CHANGELINGZERGLING,
    UnitTypeId.CHANGELINGZERGLINGWINGS,
    UnitTypeId.BROODLING,
    UnitTypeId.PARASITICBOMBDUMMY,  # wtf is this?
    UnitTypeId.LOCUSTMP,
    UnitTypeId.LOCUSTMPFLYING,
    # Terran
    UnitTypeId.MULE,
    UnitTypeId.KD8CHARGE,
    # Protoss
    # Adept is tricky, since the phase shift is temporary but
    # it should still be counted as an adept. just not twice.
    UnitTypeId.ADEPTPHASESHIFT,
    UnitTypeId.DISRUPTORPHASED,
}
