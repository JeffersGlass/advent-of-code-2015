import re

with open("day12/data.txt", "r") as f:
    data = f.readlines()

number_pattern = re.compile("-?\d+")
red = re.compile("red")

def process_line(line: s):
    total = 0
    while True:
        red_count = 0
        next_number = re.search(number_pattern, line)
        if not next_number: break
        next_red = re.search(red, line)
        next_close = re.search("\{", line)

        #number next
        if next_number.pos < min(next_red.pos, next_close.pos):
            if red_count == 0: total += int(next_number.group())
            line = line[next_number.span[1]:]
        elif next_red < min(next_number.pos, next_close.pos):
            red_count += 1
            line = line[next_red.span[1]:]
        elif next_close < min(next_number.pos, next_red.pos):
            red_count = max(red_count-1, 0)
            line = line[next_close.span[1]:]
    return total


print(process_line("[1,2,3]"))
        

    
    


    
    

print(total)