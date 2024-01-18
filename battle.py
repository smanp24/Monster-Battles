from __future__ import annotations
from enum import auto
from typing import Optional

from base_enum import BaseEnum
from team import MonsterTeam


class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    def __init__(self, verbosity=0) -> None:
        self.verbosity = verbosity

    def process_turn(self) -> Optional[Battle.Result]:
        """
        Process a single turn of the battle. Should:
        * process actions chosen by each team
        * level and evolve monsters
        * remove fainted monsters and retrieve new ones.
        * return the battle result if completed.
        """
        t1_action = self.team1.choose_action(self.out1, self.out2)
        t2_action = self.team2.choose_action(self.out2, self.out1)

        if t1_action == Battle.Action.SWAP:
            self.out1 = self.team1.retrieve_from_team()
        elif t1_action == Battle.Action.SPECIAL:
            self.team1.special()
            self.out1 = self.team1.retrieve_from_team()

        if t1_action == Battle.Action.SWAP:
            self.out1 = self.team1.retrieve_from_team()
        elif t1_action == Battle.Action.SPECIAL:
            self.team1.special()
            self.out1 = self.team1.retrieve_from_team()

        if t1_action == Battle.Action.ATTACK and t2_action == Battle.Action.ATTACK:
            pass

        if t1_action == Battle.Action.ATTACK:
            pass

        self.out1.hp -= 1
        self.out2.hp -= 1

        if self.out1.hp <= 0:
            self.out1 = self.team1.retrieve_from_team()
        if self.out2.hp <= 0:
            self.out2 = self.team2.retrieve_from_team()

        if len(self.team1) == 0:
            return Battle.Result.TEAM1
        if len(self.team2) == 0:
            return Battle.Result.TEAM2

        return None


    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = team1.retrieve_from_team()
        self.out2 = team2.retrieve_from_team()
        result = None
        while result is None:
            result = self.process_turn()
        # Add any postgame logic here.
        return result

if __name__ == "__main__":
    t1 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    t2 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    b = Battle(verbosity=3)
    print(b.battle(t1, t2))
