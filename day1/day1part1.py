with open("day1/data.txt", "r") as f:
    data = f.read()

print(f"Floor: {data.count('(') - data.count(')')}")

