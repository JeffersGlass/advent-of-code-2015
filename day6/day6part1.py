from dataclasses import dataclass
from enum import Enum, auto
import itertools

with open("day6/data.txt", "r") as f:
    instructions = f.readlines()

class State(Enum):
    ON = auto()
    OFF = auto()

    @staticmethod
    def toggle(s):
        if s == State.ON: return State.OFF
        return State.ON

class InstState(Enum):
    SET_ON = auto()
    SET_OFF = auto()
    TOGGLE = auto()

@dataclass
class Rectangle:
    left: int
    right: int
    top: int
    bottom: int

    def split_x(self, x) -> list["Rectangle"]:
        print(f"Called split_x({x}) on {self}")

        
    def split_y(self, y) -> list["Rectangle"]:
        print(f"Called split_y({y}) on {self}")
        if y < self.top or y > self.bottom: return [self]
    
@dataclass
class Instruction:
    rect: Rectangle
    state: InstState

@dataclass
class LightRectangle:
    rect: Rectangle
    state: State

    def overlaps(self, other: "LightRectangle"):
        if self.rect.bottom < other.rect.top or self.rect.top > other.rect.bottom: return False
        if self.rect.right < other.rect.left or self.rect.left > other.rect.right: return False
        return True
    
    def apply(self, instruction: Instruction) -> list["LightRectangle"]:
        other = instruction
        if not self.overlaps(other): return [self]

        left = max(self.rect.left, other.rect.left)
        right = min(self.rect.right, other.rect.right)
        top = max(self.rect.top, other.rect.top)
        bottom = min(self.rect.bottom, other.rect.bottom)
        overlap = Rectangle(left, right, top, bottom)

        if instruction.state == InstState.SET_ON: new_state = State.ON
        elif instruction.state == InstState.SET_OFF: new_state = State.OFF
        elif instruction.state == InstState.TOGGLE: new_state = State.toggle(self.state)
        else: raise ValueError(f"Unknown instruction {instruction}")

        returns = [LightRectangle(Rectangle(left, right, top, bottom), new_state)]
        print("New overlap rect: ", returns)
        if left == self.rect.left and right == self.rect.right and top == self.rect.top and bottom == self.rect.bottom:
            return returns

        next_rects = self.rect.split_x(left)
        print("After first split x: ", next_rects, "\n")
        next_rects = [x for r in next_rects for x in r.split_x(right)]
        print("After second split x: ", next_rects, "\n")
        next_rects = [x for r in next_rects for x in r.split_y(top)]
        print("After first split y: ", next_rects, "\n")
        next_rects = [x for r in next_rects for x in r.split_y(bottom)]
        print("After second split y: ", next_rects, "\n")
        returns.extend([LightRectangle(Rectangle(r.left, r.right, r.top, r.bottom), self.state) for r in next_rects if r != instruction.rect])

        return returns
    
    def count_lights(self):
        if self.state == State.OFF: return 0
        return (self.rect.right - self.rect.left + 1) * (self.rect.bottom - self.rect.top + 1)


if __name__ == "__main__":

    a = LightRectangle(Rectangle(0, 10, 0, 10), State.OFF)
    b = LightRectangle(Rectangle(0, 2, 0, 2), State.OFF)
    assert a.overlaps(b)

    # Instruction that doesn't overlap
    w = Instruction(Rectangle(200, 201, 200, 201), InstState.SET_ON)
    result = a.apply(w)
    assert result == [a]
    
    x = Instruction(Rectangle(0, 0, 0, 0), InstState.SET_ON)
    result = a.apply(x)
    print("\n".join(str(r) for r in result))
    assert len(result) == 4

    exit()



    rects = [LightRectangle(Rectangle(0, 999, 0, 999), State.OFF)]
    new = []
    insts = [
        Instruction(Rectangle(0, 999, 0, 999), InstState.SET_ON),
        Instruction(Rectangle(0, 999, 0, 0), InstState.TOGGLE),

    ]
    for i in insts:
        for r in rects:
            new.extend(r.apply(i))
        rects = new
        new = []

    print("\n".join(str(r) for r in rects))
    print(f"Total lights: {sum(r.count_lights() for r in rects)}")

    #rects = [LightRectangle(0, 0, 999, 999, State.OFF)]
    # for inst in parsed instructions:
    #       for rect in rects:
    #            rect.apply(inst)

