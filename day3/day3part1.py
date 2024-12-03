with open("day3/data.txt", "r") as f:
    data = f.read()



location = (0, 0)
houses = set([location])

for char in data:
    if char == "^":
        location = (location[0], location[1]-1)
    elif char == ">":
        location = (location[0] + 1, location[1])
    elif char == "v":
        location = (location[0], location[1] + 1)
    elif char == "<":
        location = (location[0] - 1, location[1])
    else:
        raise ValueError(f"Unrecognized character {char}")
    
    houses.add(location)

print(f"{len(houses)=}")

