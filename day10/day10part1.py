import re

pattern = re.compile(r"^(\d)\1*")



def say_it(s: str) -> str:
    result = ""
    while (s):
        starting_numbers = re.match(pattern, s)
        if not starting_numbers:
            raise ValueError(f"No match for {s}")
        span = starting_numbers.span()
        result += str((span[1] - span[0])) + starting_numbers.group()[0]
        #print(f"{s=: <20}{starting_numbers.group(): <5}{result=: <20}{span}")
        if span[1] == len(s): break
        s = s[span[1]:]
    return result

x = "1113122113"
for _ in range(40):
    print(_)
    x = say_it(x)
print(len(x))
