with open("day1/data.txt", "r") as f:
    data = f.read()

floor = 0
for i, char in enumerate(data):
    if char == "(": floor += 1
    elif char == ")": floor -= 1
    if floor < 0: 
        print(f"Entered basement on step {i+1}")
        break

