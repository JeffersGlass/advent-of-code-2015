import re

with open("day12/data.txt", "r") as f:
    data = f.readlines()

pattern = re.compile("-?\d+")

total = 0
for line in data:
    numbers = re.findall(pattern, line)
    total += sum(int(n) for n in numbers)

print(total)