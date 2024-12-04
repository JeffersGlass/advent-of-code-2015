from dataclasses import dataclass
from enum import Enum, auto
import re

with open("day6/data.txt", "r") as f:
    instructions = f.readlines()

class State(Enum):
    ON = 0
    OFF = 1

    @staticmethod
    def toggle(s):
        if s == State.ON: return State.OFF
        return State.ON

class InstState(Enum):
    SET_ON = auto()
    SET_OFF = auto()
    TOGGLE = auto()

@dataclass
class LightRange:
    line: int
    start: int
    end: int
    state: State

    def apply(self, other: "LightRange", inst: InstState ) -> list["LightRange"]:
        # Different lines
        if other.line != line: return [self]

        #No Overlap
        if other.end < self.start or other.start > self.end: return [self]

        # Applied range fully covers self
        if other.start <= self.start and other.end >= self.end:
            if inst == InstState.SET_ON: self.state = State.ON
            elif inst == InstState.SET_OFF: self.state = State.OFF
            elif inst == InstState.TOGGLE: self.state = State.toggle(self.state)
            else: raise ValueError(f"Unknown instruction {inst}")

        #


pattern = re.compile(r"(?P<inst>turn off|turn on|toggle) (?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)")

if __name__ == "__main__":
    lights_on = list()

    for line in instructions:
        m = re.match(pattern, line)


"""
turn off 660,55 through 986,197
turn off 341,304 through 638,850
turn off 199,133 through 461,193
toggle 322,558 through 977,958
toggle 537,781 through 687,941
turn on 226,196 through 599,390
turn on 240,129 through 703,297
turn on 317,329 through 451,798
turn on 957,736 through 977,890
"""
