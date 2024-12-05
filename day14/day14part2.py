from dataclasses import dataclass
from enum import Enum, auto
import re
import operator


class State(Enum):
    FLYING = auto()
    RESTING = auto()


@dataclass
class Reindeer:
    name: str
    speed: int
    flight_capacity: int
    rest_capcity: int
    location: int = 0
    duration_in_phase: int = 0
    phase: State = State.FLYING
    score: int = 0

    def pass_a_second(self):
        self.duration_in_phase += 1
        if self.phase == State.FLYING:
            self.location += self.speed
            if self.duration_in_phase >= self.flight_capacity:
                self.phase = State.RESTING
                self.duration_in_phase = 0

        elif self.phase == State.RESTING:
            if self.duration_in_phase >= self.rest_capcity:
                self.phase = State.FLYING
                self.duration_in_phase = 0


pattern = re.compile(
    r"(?P<name>\w+) can fly (?P<speed>\d+) km/s for (?P<flight_capacity>\d+) seconds, but then must rest for (?P<rest_capcity>\d+) seconds."
)

with open("day14/data.txt", "r") as f:
    data = f.readlines()

reindeer: list[Reindeer] = []
for line in data:
    m = re.match(pattern, line)
    reindeer.append(
        Reindeer(
            name=m.group("name"),
            speed=int(m.group("speed")),
            flight_capacity=int(m.group("flight_capacity")),
            rest_capcity=int(m.group("rest_capcity")),
        )
    )

#FLY!
for i in range(2503):
    for deer in reindeer:
        deer.pass_a_second()
    next(r for r in sorted(reindeer, key = operator.attrgetter('location'), reverse=True)).score += 1


winner = next(r for r in sorted(reindeer, key = operator.attrgetter('score'), reverse=True))
print(f"{winner.name} is the winner with {winner.score} points")



