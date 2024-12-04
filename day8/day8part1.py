import string
from colored import Fore, Style

def cprint(s: str, *args, **kwargs):
    mod = 0
    temp_end = kwargs['end'] if 'end' in kwargs else "\n"
    kwargs['end'] = ''
    for char in s:
        before = ''
        if mod == 9: before = Fore.green
        elif mod == 4: before = Fore.red
        elif mod == 0 or mod == 5: before = Style.reset
        print(f"{before}{char}", *args, **kwargs)
        mod = (mod + 1) % 10 
    if temp_end is not None: print("", end=temp_end)

def memory_size(line:str):
    cprint(f"{line: <50} {len(line)=: <8} ", end = "")
    line = line.strip('"')
    count = 0
    nonstandard = 0

    while True:
        if not line: break
        first = line[0]
        if len(line) >= 2 and first == "\\" and line[1] == "\\":
            count += 1
            nonstandard += 1 
            line = line[2:]
        elif len(line) >= 2 and first == '\\' and line[1] == '"':
            count += 1
            nonstandard += 1 
            line = line[2:]
        elif len(line) >= 4 and first == '\\' and line[1] == 'x' and line[2] in string.hexdigits and line[3] in string.hexdigits:
            count +=1
            nonstandard += 1 
            line = line[4:]
        else:
            count += 1
            line = line[1:]
        
    cprint(f"{count=} {nonstandard=}")
    return count

def test_parse_line():
    assert memory_size("") == 0
    assert memory_size("abc") == 3
    assert memory_size('aaa\\"aaa') == 7
    assert memory_size("\\x27") == 1
    assert memory_size('yustxxtot\\"muec\\"xvfdbzunzvveq') == 28
    assert memory_size('gf\\"tssmvm\\"gm\\"hu\\x9a\\xb7yjawsa') == 23
    assert memory_size('"aq\\\\aurmbhy"') == 11
    assert memory_size('"pxunovbbrrn\\\\vullyn\\"bno\\"\\"\\"myfxlp\\""') == 33

if __name__ == "__main__":
    with open("day8/data.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]

    print(sum(len(line) - memory_size(line) for line in lines))