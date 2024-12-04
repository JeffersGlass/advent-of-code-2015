import re
import logging

with open("day12/data.txt", "r") as f:
    data = f.readlines()

number_pattern = re.compile(r"-?\d+")
red = re.compile("red")

def process_line(line: str):
    total = 0
    red_count = 0
    while True:
        next_number = re.search(number_pattern, line)
        if not next_number: break
        next_number_pos = next_number.span()[0]
        next_red = re.search(red, line)
        next_red_pos = next_red.span()[0] if next_red else float("inf")

        next_close = re.search("{", line)
        next_close_pos = next_close.span()[0] if next_close else float("inf")

        #number next
        if next_number_pos < min(next_red_pos, next_close_pos):
            if red_count <= 0: total += int(next_number.group())
            print(f"{red_count=}, adding {next_number.group()} to total")
            line = line[next_number.span()[1]:]
        elif next_red_pos < min(next_number_pos, next_close_pos):
            red_count += 1
            print(f"Found red at position {next_red_pos}, {red_count=}")
            line = line[next_red.span()[1]:]
        elif next_close_pos< min(next_number_pos, next_red_pos):
            red_count = max(red_count-1, 0) # THIS IS WRONG
            line = line[next_close.span()[1]:]
        else:
            raise ValueError(f"No progress made, {next_number=} {next_red=} {next_close=}")
    return total

def test_process_line():
    assert process_line("[1,2,3]") == 6
    assert process_line('[1,{"c":"red","b":2},3]') == 4

print(process_line('[1,{"c":"red","b":2},3]'))