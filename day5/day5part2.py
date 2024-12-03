from collections import Counter
import re

repeated_pair = re.compile(r"(\w)(\w).*\1\2")
one_space = re.compile(r"(\w).\1")

def is_nice(s: str):
    return re.search(repeated_pair, s) and re.search(one_space, s)

with open("day5/data.txt", "r") as f:
    data = f.readlines()

print(f"Total nice lines: {sum(1 if is_nice(line) else 0 for line in data)}")