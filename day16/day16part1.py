from dataclasses import dataclass
import re

@dataclass
class SueData:
    children: int | None = None
    cats: int | None = None
    samoyeds: int | None = None
    pomeranians: int | None = None
    akitas: int | None = None
    vizslas: int | None = None
    goldfish: int | None = None
    trees: int | None = None
    cars: int | None = None
    perfumes: int | None = None

    def __eq__(self, other: 'SueData'):
        return not any(getattr(self, att) is not None and getattr(other, att) is  not None for att in self.__annotations__.keys())

with open("day16/data_ticker.txt", "r") as f:
    ticker = f.readlines()

base = SueData()
base_pattern = re.compile(r"(?P<attr>\w+): (?P<num>\d+)")
for line in ticker:
    m = re.match(base_pattern, line)
    if not m: raise ValueError(f"Unparsable line {line}")

    setattr(base, m.group('attr'), int(m.group('num')))

with open("day16/data_sues.txt", "r") as f:
    sues_data = f.readlines()

sues = [] 
for line in sues_data:
    sue_part, data_part = line.split(":", 1)
    sue_num = sue_part.split(" ")[1]
    single_data = {}
    for section in data_part.strip().split(","):
        name, number = section.split(":")
        single_data[name] = int(number)
    sues.append(SueData(*single_data))

print(next(sue for sue in sues if sue == base))