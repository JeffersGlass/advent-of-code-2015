from dataclasses import dataclass
import functools
import operator
from typing import Callable
import re

@dataclass
class Wire:
    name: str
    def emit_value(self):
        pass

@dataclass
class LiteralWire(Wire):
    value: int

    def emit_value(self):
        return self.value


@dataclass
class ArithmeticWire(Wire):
    op: Callable
    parents: list[str]

    def emit_value(self):
        print(f"Getting value for wire {self.name} with op {self.op} and parents {self.parents}")
        real_parents = [wires[p] for p in self.parents]
        return op(*[p.emit_value() for p in real_parents])


wires: dict[str, Wire] = {}
wires['1'] = LiteralWire(name = '1', value=1)

with open("day7/data.txt", "r") as f:
    lines = f.readlines()

pattern = r"((NOT (?P<not_target>\w+))|(?P<literal>\d+)|(?P<one>\w+) (?P<op>OR|AND) (?P<two>\w+)|((?P<shift_target>\w+) (?P<shift_type>LSHIFT|RSHIFT) (?P<shift_value>\d+))|(?P<solo>\w+)) -> (?P<target>\w+)"

for inst in lines:
    m = re.match(pattern, inst)
    name = m.group('target')
    
    if t:= m.group('not_target'):
        op = operator.invert
        parents = t
        wires[name] = ArithmeticWire(name = name, op = op, parents=parents)
    elif v:= m.group('literal'):
        wires[name] = LiteralWire(name = name, value = int(v))
    elif one := m.group('one'):
        parents = [one, m.group('two')]
        if (op:= m.group('op')) == 'OR': op = operator.or_
        elif op == 'AND' : op = operator.and_
        else: raise ValueError(f"Unknown binary operator {op}")
        wires[name] = ArithmeticWire(name = name, op = op, parents = parents)
    elif shift_target := m.group('shift_target'):
        value = int(m.group('shift_value'))
        if m.group('shift_type') == 'LSHIFT': op = lambda x: x << value
        elif m.group('shift_type') == 'RSHIFT': op = lambda x : x >> value
        else: raise ValueError(f"Unknown shift type {m.group('shift_type')}")
        wires[name] = ArithmeticWire(name = name, op = op, parents = [shift_target])
    elif solo:= m.group('solo'):
        op = operator.itemgetter(0)
        parents = [solo]
        wires[name] = ArithmeticWire(name = name, op = op, parents=parents)
    else:
        raise ValueError(f'Unacceptable line {inst}')
        
for w, v in wires.items():
    print(w, v)


print(wires['a'].emit_value())

