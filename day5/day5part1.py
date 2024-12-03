from collections import Counter
import re

vowels = "aeiou"
forbidden = "ab", "cd", "pq", "xy"
double_letter = re.compile(r"(\w)\1")

def is_nice(s: str):
    vowel_counts = Counter(s)
    return sum(vowel_counts[v] for v in vowels) >= 3 and \
    not any(f in s for f in forbidden) and \
    re.search(double_letter, s)

with open("day5/data.txt", "r") as f:
    data = f.readlines()

print(f"Total nice lines: {sum(1 if is_nice(line) else 0 for line in data)}")