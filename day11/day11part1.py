def to_number(s: str) -> list[int]:
    return [ord(s)-ord('a') for s in s]

def to_word(p: list[int]) -> str:
    return ''.join(chr(num + ord('a')) for num in p)

def is_valid(p: list[int]) -> bool:
    pass
    # Includes straight line of increasing letters like bcd, xyz
    # May not contain i, o, or l
    # must contain at least two different, non-overlapping pairs like aa, bb, zz


def increment_pass(p: list[int]) -> list[int]:
    result = [x for x in p]
    for i in range(7, -1, -1):
        result[i] += 1
        if i < 26: break
        result[i] = 0
    return result

start = "vzbxkghb"

