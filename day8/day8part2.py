def escape_line(line: str):
    return len(line.strip()) + line.count("\\") + line.count("\"") + 2

def test_escape_line():
    assert escape_line('""') == 6
    assert escape_line('"abc"') == 9
    assert escape_line('"aaa\\"aaa"') == 16
    assert escape_line('"\\x27"') == 11
    assert len('"\\x27"') == 6


if __name__ == "__main__":
    with open("day8/data.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]

    print(sum(escape_line(line) - len(line) for line in lines))

