import re

pattern = re.compile(r"(\d)\1*")

def transform(s: str) -> str:
    matches = re.finditer(pattern, s)
    s = "".join(str((m.span()[1] - m.span()[0])) + m.group()[0] for m in matches)
    return s
    

x = "1113122113"
for _ in range(50):
    print("Step", _)
    x = transform(x)
print(len(x))
