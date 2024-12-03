with open("day2/data.txt", "r") as f:
    data = f.readlines()

total = 0
for line in data:
    box = [int(d) for d in line.strip().split("x")]
    perimeters = [2* box[0] +  2*box[1], 2*box[1] + 2*box[2], 2*box[2] + 2*box[0]]
    ribbon = min(perimeters)
    total += ribbon + box[0]*box[1]*box[2]

print(f"Total: {total}")