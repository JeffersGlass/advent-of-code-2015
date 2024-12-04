import re

not_allowed = ['i', 'o', 'l']
doubles = re.compile(r'(\w)\1.*(\w)\2')

def is_valid(p: str) -> bool:
    # May not contain i, o, or l
    # Includes straight line of increasing letters like bcd, xyz
    """print(p, end = "\t")
    if any(n in p for n in not_allowed):
        print("Disallowed letter includes")
        return False
    if not (any((ord(p[n]) == ord(p[n+1])-1 == ord(p[n+2])-2) for n in range(6))):
        print("No run of continuous letters")
        return False
    if not ((m:= re.search(doubles, p)) and (m.group(1) != m.group(2))):
        print("No double letters")
        return False
    return True """
    
    
    return (not any(n in p for n in not_allowed)) and \
        (any((ord(p[n]) == ord(p[n+1])-1 == ord(p[n+2])-2) for n in range(6))) and \
        ((m:= re.search(doubles, p)) and (m.group(1) != m.group(2)))
    
    
    # must contain at least two different, non-overlapping pairs like aa, bb, zz


def increment_pass(p: str) -> str:
    result = list(p)
    for i in range(7, -1, -1):
        result[i] = chr(ord(result[i]) + 1)
        if ord(result[i]) <= ord('z'): break
        result[i] = 'a'
    return ''.join(result)

def find_next(p: str) -> str:
    while not is_valid(p):
        #input()
        p = increment_pass(p)
    return p

def test_find_next():
    assert find_next("abcdefgh") == "abcdffaa"

if __name__ == "__main__":
    # part 1
    print(find_next("vzbxkghb"))

    # part 2
    print(find_next(increment_pass("vzbxxyzz")))
