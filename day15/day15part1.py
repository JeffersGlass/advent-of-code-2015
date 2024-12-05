from collections import namedtuple
import math
import re
from typing import Generator

pattern = re.compile(r"(?P<name>\w+): capacity (?P<capacity>-?\d+), durability (?P<durability>-?\d+), flavor (?P<flavor>-?\d+), texture (?P<texture>-?\d+), calories (?P<calories>-?\d+)")

Ingredient = namedtuple("Ingredient", ['capacity', 'durability', 'flavor', 'texture', 'calories', 'name'])
properties: list[Ingredient] = []

def combinations_2(size: int) -> Generator[tuple[int, int]]:
    for a in range(0, 100+1):
        yield (a, size-a)

def combinations_4(size: int) -> Generator[tuple[int, int, int, int]]:
    for a in range(0, 100+1):
        for b in range(0, 100+1-a):
            for c in range(0, 100+1-a-b):
                yield(a, b, c, size - a - b - c)

if __name__ == "__main__":
    with open("day15/data.txt", "r") as f:
        data = f.readlines()


    for line in data:
        m = re.match(pattern, line)
        if not m: raise ValueError(f"Could not match line: {line}")
        properties.append(Ingredient(
            capacity=int(m.group('capacity')),
            durability=int(m.group('durability')),
            flavor=int(m.group('flavor')),
            texture=int(m.group('texture')),
            calories=int(m.group('calories')),
            name = m.group('name')
        ))

    largest = float('-inf')

    for combo in combinations_4(100):
        values = [sum(properties[x][i] * combo[x] for x in range(len(combo))) for i in range(4)]
        score = math.prod(values) if not any(v < 0 for v in values) else 0
        largest = max(largest, score)
    print(largest)
        

