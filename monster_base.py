from __future__ import annotations
import abc
import math

from elements import EffectivenessCalculator, Element
from stats import Stats

class MonsterBase(abc.ABC):

    def __init__(self, simple_mode=True, level: int = 1) -> None:
        """
        Initialise an instance of a monster.

        :simple_mode: Whether to use the simple or complex stats of this monster
        :level: The starting level of this monster. Defaults to 1.
        """
        self.simple_mode = simple_mode
        self.orig_level = level
        self.level = level
        self.hp = self.get_max_hp()
        self.max_hp = self.get_max_hp()

    def get_level(self):
        """The current level of this monster instance"""
        return self.level

    def level_up(self):
        """Increase the level of this monster instance by 1"""
        difference = self.max_hp - self.hp
        self.level += 1
        self.hp = self.get_max_hp() - difference

    def get_hp(self):
        """Get the current HP of this monster instance"""
        return self.hp

    def set_hp(self, val):
        """Set the current HP of this monster instance"""
        self.hp = val

    def get_attack(self):
        """Get the attack of this monster instance"""
        return self.get_simple_stats().get_attack()

    def get_defense(self):
        """Get the defense of this monster instance"""
        return self.get_simple_stats().get_defense()

    def get_speed(self):
        """Get the speed of this monster instance"""
        return self.get_simple_stats().get_speed()

    def get_max_hp(self):
        """Get the maximum HP of this monster instance"""
        return self.get_simple_stats().get_max_hp()

    def alive(self) -> bool:
        """Whether the current monster instance is alive (HP > 0 )"""
        return self.get_hp() > 0

    def attack(self, other: MonsterBase):
        """Attack another monster instance"""
        # Step 1: Compute attack stat vs. defense stat
        # Step 2: Apply type effectiveness
        # Step 3: Ceil to int
        # Step 4: Lose HP
        damage = 0
        defense = self.get_defense()
        attack = other.get_attack()
        if defense < attack / 2:
            damage = attack - defense
        elif defense < attack:
            damage = (attack * 5 / 8) - (defense / 4)
        else:
            damage = attack / 4

        element = self.get_element()
        enemy_element = other.get_element()
        damage_factor = EffectivenessCalculator.get_effectiveness(Element.from_string(element),
                                                                  Element.from_string(enemy_element))
        effective_damage = math.ceil(damage * damage_factor)
        other.hp = other.hp - effective_damage

    def ready_to_evolve(self) -> bool:
        """Whether this monster is ready to evolve. See assignment spec for specific logic."""
        if self.get_evolution() is not None:
            if self.level > self.orig_level:
                return True
            else:
                return False
        return False

    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        evolved_class = self.get_evolution()
        evolved_monster = evolved_class(simple_mode=True, level=self.level)
        evolved_monster.max_hp = evolved_monster.get_max_hp()
        evolved_monster.hp = evolved_monster.max_hp - (self.get_max_hp() - self.hp)
        return evolved_monster

    def __str__(self):
        return f"LV.{self.level} {self.get_name()}, {self.hp}/{self.max_hp} HP"

    ### NOTE
    # Below is provided by the factory - classmethods
    # You do not need to implement them
    # And you can assume they have implementations in the above methods.

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Returns the name of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_description(cls) -> str:
        """Returns the description of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_evolution(cls) -> type[MonsterBase]:
        """
        Returns the class of the evolution of the Monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_element(cls) -> str:
        """
        Returns the element of the Monster.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def can_be_spawned(cls) -> bool:
        """
        Returns whether this monster type can be spawned on a team.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_simple_stats(cls) -> Stats:
        """
        Returns the simple stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_complex_stats(cls) -> Stats:
        """
        Returns the complex stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass


