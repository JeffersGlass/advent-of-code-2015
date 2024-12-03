with open("day2/data.txt", "r") as f:
    data = f.readlines()

total = 0
for line in data:
    box = [int(d) for d in line.strip().split("x")]
    sides = [box[0] * box[1], box[1] * box[2], box[2] * box[0]]
    smallest = min(sides)
    total += sum(2 * side for side in sides) + smallest

print(f"Total: {total}")