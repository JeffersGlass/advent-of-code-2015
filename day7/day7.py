from dataclasses import dataclass
import operator
from typing import Callable
import re
from textwrap import dedent

@dataclass
class Wire:
    name: str
    def emit_value(self):
        pass

@dataclass
class LiteralWire(Wire):
    cached_value:int | None = None

    def __post_init__(self):
        pass
        #print(f"Literal cached value for {self.name: <2} {self.cached_value}")


    def emit_value(self):
        #print(f"Emitting literal value {self.value}")
        return self.cached_value


@dataclass
class ArithmeticWire(Wire):
    op: Callable
    parents: list[str]
    wires: list[Wire]
    cached_value:int | None = None
    

    def emit_value(self) -> int:
        if self.cached_value is not None: 
            #print(f"Using cached value for wire {self.name}")
            if self.cached_value > 2**16: raise ValueError("AHA!")
            return self.cached_value
        #print(f"Getting value for wire {self.name} with op {self.op} and parents {self.parents}")
        #print(f"Op is {getsource(op).strip()}")
        real_parents = [self.wires[p] for p in self.parents]
        if all(p.cached_value is not None for p in real_parents):
            self.cached_value = self.op(*[p.emit_value() for p in real_parents])
            #print(f"New cached value for {self.name: <2} {self.cached_value}")
            if self.cached_value > 2**16: raise ValueError("AHA!")
            return self.cached_value
        else:
            raise RecursionError(f"Some children of {self.__class__.__name__} {self.name} do not have fixed values: {[p.name for p in real_parents if not p.cached_value]}")
        
def parents_are_usable(a: ArithmeticWire, finished: list[str]) -> bool:
    if not hasattr(a, 'parents'): return True
    return all(p in finished for p in a.parents)

pattern = r"((NOT (?P<not_target>\w+))|(?P<literal>\d+)|(?P<one>\w+) (?P<op>OR|AND) (?P<two>\w+)|((?P<shift_target>\w+) (?P<shift_type>LSHIFT|RSHIFT) (?P<shift_value>\d+))|(?P<solo>\w+)) -> (?P<target>\w+)"

def load_lines(lines: list[str]) -> dict[str, Wire]:

    wires: dict[str, Wire] = {}
    wires['1'] = LiteralWire(name = '1', cached_value=1)

    for inst in lines:
        m = re.match(pattern, inst)
        if not m: raise ValueError(f"Line did not match instruction regex: '{inst}'")
        name = m.group('target')
    
        
        if t:= m.group('not_target'):
            op = operator.invert
            parents = [t]
            wires[name] = ArithmeticWire(name = name, op = op, wires = wires, parents=parents)
        elif v:= m.group('literal'):
            wires[name] = LiteralWire(name = name, cached_value = int(v))
        elif one := m.group('one'):
            parents = [one, m.group('two')]
            if (op:= m.group('op')) == 'OR': op = operator.or_
            elif op == 'AND' : op = operator.and_
            else: raise ValueError(f"Unknown binary operator {op}")
            wires[name] = ArithmeticWire(name = name, op = op, wires = wires, parents = parents)
        elif shift_target := m.group('shift_target'):
            shift_value = int(m.group('shift_value'))
            if m.group('shift_type') == 'LSHIFT': op = lambda x, value=shift_value: x << value
            elif m.group('shift_type') == 'RSHIFT': op = lambda x, value=shift_value: x >> value
            else: raise ValueError(f"Unknown shift type {m.group('shift_type')}")
            wires[name] = ArithmeticWire(name = name, op = op, wires=wires, parents = [shift_target])
            wires[name].shift_value = shift_value
        elif solo:= m.group('solo'):
            op = lambda x: x
            parents = [solo]
            wires[name] = ArithmeticWire(name = name, op = op, wires=wires, parents=parents)
        else:
            raise ValueError(f'Unacceptable line {inst}')
    return wires
        
def process_wires(wires: dict[str, Wire], endwire: str):
    finished = set()

    while not wires[endwire].cached_value:
        print("-")
        #print(f"Starting loop with {len([w for w in wires if w not in finished])} wires to check")
        updated = 0
        for wire in [w for w in wires if w not in finished]:
            if wires[wire].cached_value is not None:
                finished.add(wire)
                updated += 1
                #print(f"New cached value found for wire {wire}")
                continue
            try:
                wires[wire].emit_value()
                finished.add(wire)
                updated += 1
            except RecursionError as err:
                pass
        if updated == 0: 
            print("====FAIL====")
            print(f"{len(finished)=}", sorted([(f, wires[f].cached_value) for f in finished], key = operator.itemgetter(0)))
            print(f"{len(wires)=}")
            solvable = [w for w in wires if parents_are_usable(wires[w], finished)]
            print("Sovlable", solvable)        
            print(f"{len(solvable)= }")
            print(f"Did not process {set(solvable) - set(finished)}")
            raise RuntimeError("Ran through all wires without updating, exitting")
    return wires[endwire].cached_value

def string_to_lines(s: str) -> list[str]:
    return [line for line in dedent(s).split("\n") if line]

if __name__ == "__main__":
    data = string_to_lines("""
                1 -> a
                """)
    assert process_wires(load_lines(data), 'a') == 1

    data = string_to_lines("""
                2 -> b
                1 OR b -> a
                """)
    assert process_wires(load_lines(data), 'a') == 3

    data = string_to_lines("""
                2 -> b
                4 -> c
                b OR c -> a
                """)
    assert process_wires(load_lines(data), 'a') == 6

    data = string_to_lines("""
                3 -> b
                1 AND b -> a
                """)
    assert process_wires(load_lines(data), 'a') == 1

    data = string_to_lines("""
                3 -> b
                5 -> c
                b AND c -> a
                """)
    assert process_wires(load_lines(data), 'a') == 1

    data = string_to_lines("""
                4 -> b
                b LSHIFT 1 -> a
                """)
    assert process_wires(load_lines(data), 'a') == 8

    data = string_to_lines("""
                4 -> b
                b RSHIFT 1 -> a
                """)
    assert process_wires(load_lines(data), 'a') == 2

    data = string_to_lines("""
                3 -> b
                NOT b -> a
                """)
    assert process_wires(load_lines(data), 'a') == -4

    print("Passed tests")

    with open("day7/data.txt", "r") as f:
        lines = f.readlines()

    #part 1
    part_1_result = process_wires(load_lines(lines), 'a')
    print(f"===== {part_1_result= } ====\n\n")

    #part 2
    new_lines = [re.sub(r"(\d+) -> b$", f"{part_1_result} -> b", line) for line in lines]
    #print("\n".join(str(line) for line in lines if "-> b" in line))
    part_2_result = process_wires(load_lines(new_lines), 'a')
    print(f"{part_2_result= }")



