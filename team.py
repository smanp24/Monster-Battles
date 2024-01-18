from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.referential_array import ArrayR

if TYPE_CHECKING:
    from battle import Battle

class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6

    def __init__(self, team_mode: TeamMode, selection_mode, **kwargs) -> None:
        # Add any preinit logic here.
        self.sort_key = None
        self.team = () 
        self.team_mode = team_mode
        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly()
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually()
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(kwargs.get('provided_monsters'), kwargs.get('sort_key'))
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")

        self.original_team = self.team

    def add_to_team(self, monster: MonsterBase):
        if self.team_mode == MonsterTeam.TeamMode.FRONT:
            self.team = (monster, ) + self.team
        elif self.team_mode == MonsterTeam.TeamMode.BACK:
            self.team = self.team + (monster, )
        elif self.team_mode == MonsterTeam.TeamMode.OPTIMISE:
            sorting_variable = None
            if self.sort_key == MonsterTeam.SortMode.HP:
                sorting_variable = "hp"
            elif self.sort_key == MonsterTeam.SortMode.ATTACK:
                sorting_variable = "attack"
            elif self.sort_key == MonsterTeam.SortMode.DEFENSE:
                sorting_variable = "defense"
            elif self.sort_key == MonsterTeam.SortMode.SPEED:
                sorting_variable = "speed"
            elif self.sort_key == MonsterTeam.SortMode.LEVEL:
                sorting_variable = "level"
            stat_value = getattr(monster, sorting_variable)
            index = 0
            for i in range(len(self.team)):
                current_stat_value = getattr(self.team[i], sorting_variable)
                if stat_value >= current_stat_value:
                    index = i
                    break

            self.team = self.team[:index] + (monster, ) + self.team[index:]

    def retrieve_from_team(self) -> MonsterBase:
        if self.team:
            retrieved_monster = self.team[0]
            self.team = self.team[1:]
            return retrieved_monster

    def special(self) -> None:
        if self.team_mode == MonsterTeam.TeamMode.FRONT:
            if len(self.team) >= 3:
                reversed_monsters = (self.team[2], self.team[1], self.team[0])
                self.team = reversed_monsters + self.team[3:]
            else:
                self.team = self.team[::-1]
        elif self.team_mode == MonsterTeam.TeamMode.BACK:
            halfway = (len(self.team)) // 2
            first_half = self.team[:halfway]
            second_half = self.team[halfway:]
            swapped_second_half = second_half[::-1]
            self.team = swapped_second_half + first_half
        elif self.team_mode == MonsterTeam.TeamMode.OPTIMISE:
            return self.team[::-1]

    def regenerate_team(self) -> None:
        self.team = self.original_team

    def select_randomly(self):
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.add_to_team(monsters[x]())
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. Example interaction:

        How many monsters are there? 2
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 38
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 2
        This monster cannot be spawned.
        Which monster are you spawning? 1
        """
        while True:
            team_size = int(input("How many monsters are there? "))
            if 1 <= team_size <= 6:
                break
            else:
                print("That is not a valid team size. ")
        monsters_list = get_all_monsters()
        print("MONSTERS ARE:")
        for i in range(len(monsters_list)):
            print(f"{i}: {monsters_list[i].__name__} {'✔️' if monsters_list[i].can_be_spawned() else '❌'}")

        for _ in range(team_size):
            while True:
                monster_type = int(input("Which monster are you spawning? "))
                if 0 <= monster_type <= len(monsters_list) and monsters_list[monster_type].can_be_spawned():
                    self.add_to_team(monsters_list[monster_type])
                    break
                else:
                    print("This monster cannot be spawned.")




    def select_provided(self, provided_monsters:Optional[ArrayR[type[MonsterBase]]]=None, sort_key: Optional[SortMode] = None):
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]
        """
        if provided_monsters is None:
            raise ValueError
        elif len(provided_monsters) > 6:
            raise ValueError("Too big.")

        if sort_key is not None:
            self.sort_key = sort_key

        for monster in provided_monsters:
            monster_instance = monster()
            if monster_instance.can_be_spawned():
                self.add_to_team(monster_instance)
            else:
                raise ValueError("Cannot be spawned.")

    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

    def __len__(self):
        return len(self.team)

if __name__ == "__main__":
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
        sort_key=MonsterTeam.SortMode.HP,
    )
    print(team)
    while len(team):
        print(team.retrieve_from_team())

    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.BACK,
        selection_mode=MonsterTeam.SelectionMode.MANUAL,
    )