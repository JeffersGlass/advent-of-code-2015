with open("day3/data.txt", "r") as f:
    data = f.read()

santa_location = (0, 0)
robot_location = (0, 0)
houses = set([santa_location])

f = iter(data)

for char in f:

    if char == "^":
        santa_location = (santa_location[0], santa_location[1]-1)
    elif char == ">":
        santa_location = (santa_location[0] + 1, santa_location[1])
    elif char == "v":
        santa_location = (santa_location[0], santa_location[1] + 1)
    elif char == "<":
        santa_location = (santa_location[0] - 1, santa_location[1])
    else:
        raise ValueError(f"Unrecognized character {char}")
    
    houses.add(santa_location)

    char = next(f)

    if char == "^":
        robot_location = (robot_location[0], robot_location[1]-1)
    elif char == ">":
        robot_location = (robot_location[0] + 1, robot_location[1])
    elif char == "v":
        robot_location = (robot_location[0], robot_location[1] + 1)
    elif char == "<":
        robot_location = (robot_location[0] - 1, robot_location[1])
    else:
        raise ValueError(f"Unrecognized character {char}")
    
    houses.add(robot_location)

print(f"{len(houses)=}")

