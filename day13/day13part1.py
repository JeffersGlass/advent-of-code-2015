import itertools
import re

with open("day13/data.txt", "r") as f:
    data = f.readlines()

pattern = re.compile(r"(?P<first>\w+) would (?P<sign>gain|lose) (?P<num>\d+) happiness units by sitting next to (?P<second>\w+).")

notes: dict[tuple[str, str], int] = {}
for line in data:
    m = re.match(pattern, line)
    value = (1 if m.group('sign') == 'gain' else -1) * int(m.group('num'))
    notes[(m.group('first'), m.group('second'))] = value
    
names = set([m[0] for m in notes] + [m[1] for m in notes])

max_score = 0
for permutation in itertools.permutations(names, len(names)):
    score = 0
    for pair in [*itertools.pairwise(permutation)] + [(permutation[-1], permutation[0])]:
        score += notes[pair]
        r = (pair[1], pair[0])
        score += notes[r]
    max_score = max(score, max_score)

print(max_score)