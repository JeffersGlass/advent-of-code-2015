from dataclasses import dataclass
import operator
import re
import itertools

@dataclass(unsafe_hash=True)
class Path:
    distance: int
    ends: tuple[str]

def load_paths(data: list[str]) -> set[Path]:
    paths = set()
    pattern = r"(?P<first>\w+) to (?P<second>\w+) = (?P<dist>\d+)"
    for line in data:
        if not (m:= re.match(pattern, line)):
            raise ValueError(f"Could not match line {line}")
        paths.add(Path(distance=int(m.group('dist')), ends=(m.group('first'), m.group('second'))))
    return paths

def get_ends_from_paths(paths: set[Path]) -> set[str]:
    ends = set()
    for p in paths:
        ends.add(p.ends[0])
        ends.add(p.ends[1])
    return ends


if __name__ == "__main__":
    with open("day9/data.txt") as f:
        lines = f.readlines()

    paths = load_paths(lines)
    ends = get_ends_from_paths(paths)
    permutations = itertools.permutations(ends, len(ends))
    
    #part 1
    acc = float("inf")
    comp_op = operator.lt

    #part 2
    acc = float("-inf")
    comp_op = operator.gt

    
    for perm in permutations:
        length = 0
        for pair in itertools.pairwise(perm):
            pair_distance = next(path for path in paths if set(pair) == set(path.ends)).distance
            length += pair_distance
        if comp_op(length, acc): acc = length
    print(acc)

    #print(sorted(combinations))
    #print("\n".join(str(p) for p in sorted(paths, key=operator.attrgetter('ends'))))
