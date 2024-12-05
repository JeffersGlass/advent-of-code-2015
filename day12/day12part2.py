import json

type JSON_PART = list | dict[str, JSON_PART] | str | int

with open("day12/data.txt", "r") as f:
    jdata = json.loads(f.read())

def sum_object(obj: JSON_PART) -> int:
    if (t:= type(obj)) == int:
        return obj
    if t == str:
        return 0
    if t == list:
        return sum(sum_object(i) for i in obj)
    elif t == dict:
        if "red" in obj.values(): return 0
        return sum(sum_object(v) for v in obj.values())
    else:
        raise ValueError(f"Unknown type {t}")
    
if __name__ == "__main__":
    print(sum_object(jdata))