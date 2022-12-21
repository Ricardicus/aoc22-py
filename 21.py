from general import *
from collections import deque
from sympy import Symbol, Eq
from sympy.solvers import solve


"""
lines = readlinesFromFile("inputs/21.txt.small")
lines = [ line.strip() for line in lines ]

#class Monkey:
#    def __init__(self, name, rule):
#        self.name = name
#        self.rule = rule
#        if isinstance(rule, int):
#            self.value = rule
#        self.waits_for = []
#    def waiting(self):


monkeys = {}

for line in lines:
    name = line.split(":")[0]
    rule = line.split(": ")[1]
    m = {"name":name, "rule": rule}
    if rule.isnumeric():
        rule = int(rule)
        m["waits"] = False
        m["val"] = rule
    else:
        rule = rule.split(" ")
        m["rule"] = rule
        m["waits"] = True
        m["waitList"] = [rule[0], rule[2]]
    monkeys[name] = m

figureOut = ["root"]
while figureOut:
    m = figureOut.pop(0)
    print(m)
    print(monkeys[m])
    print(figureOut)
    if monkeys[m]["waits"]:
        m1 = monkeys[m]["waitList"][0]
        m2 = monkeys[m]["waitList"][1]

        if monkeys[m1]["waits"]:
            if m1 not in figureOut:
                figureOut.append(m1)
        if monkeys[m2]["waits"]:
            if m2 not in figureOut:
                figureOut.append(m2)

        if not monkeys[m1]["waits"] and not monkeys[m2]["waits"]:
            v = 0
            r = monkeys[m]["rule"][1]
            if r == "+":
                monkeys[m]["val"] = monkeys[m1]["val"] + monkeys[m2]["val"]
            elif r == "-":
                monkeys[m]["val"] = monkeys[m1]["val"] - monkeys[m2]["val"] 
            elif r == "/":
                monkeys[m]["val"] = monkeys[m1]["val"] / monkeys[m2]["val"]
            elif r == "*":
                monkeys[m]["val"] = monkeys[m1]["val"] * monkeys[m2]["val"]
            monkeys[m]["waits"] = False
        elif m not in figureOut:
            figureOut.append(m)

print(monkeys)
print("==")
print(monkeys["root"])

"""
# Part 2
lines = readlinesFromFile("inputs/21.txt")
lines = [ line.strip() for line in lines ]

#class Monkey:
#    def __init__(self, name, rule):
#        self.name = name
#        self.rule = rule
#        if isinstance(rule, int):
#            self.value = rule
#        self.waits_for = []
#    def waiting(self):

class MagicNumber:
    def __init__(self, s = None):
        self.x = Symbol('x')
        if s is not None:
            self.x = s
    def getX(self):
        return self.x
    def __add__(self, other):
        if isinstance(other, int):
            s = self.x + other
            return MagicNumber(s)
        elif isinstance(other, MagicNumber):
            s = self.x + other.getX()
            return MagicNumber(s)
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            s = self.x - other
            return MagicNumber(s)
        elif isinstance(other, MagicNumber):
            s = self.x - other.getX()
            return MagicNumber(s)
    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, int):
            s = self.x * other
            return MagicNumber(s)
        elif isinstance(other, MagicNumber):
            s = self.x * other.getX()
            return MagicNumber(s)
    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, int):
            s = self.x / other
            return MagicNumber(s)
        elif isinstance(other, MagicNumber):
            s = self.x / other.getX()
            return MagicNumber(s)

    def __rdiv__(self, other):
        return self.__div__(other)

    def __truediv__(self, other):
        if isinstance(other, int):
            s = self.x / other
            return MagicNumber(s)
        elif isinstance(other, MagicNumber):
            s = self.x / other.getX()
            return MagicNumber(s)
        return NotImplemented

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __floordiv__(self, other):
        if isinstance(other, int):
            s = self.x / other
            return MagicNumber(s)
        elif isinstance(other, MagicNumber):
            s = self.x / other.getX()
            return MagicNumber(s)

    def __rfloordiv__(self, other):
        return self.__floordiv__(other)

    def __str__(self):
        return self.x
    def __repr__(self):
        return self.x

monkeys = {}

for line in lines:
    name = line.split(":")[0]
    rule = line.split(": ")[1]
    m = {"name":name, "rule": rule}

    if name == "root":
        rule = rule.split(" ")
        rule[1] = "="
        m["rule"] = rule
        m["waits"] = True
        m["waitList"] = [rule[0], rule[2]]
    elif name == "humn":
        m["waits"] = False
        m["val"] = Symbol('x')
    elif rule.isnumeric():
        rule = int(rule)
        m["waits"] = False
        m["val"] = rule
    else:
        rule = rule.split(" ")
        m["rule"] = rule
        m["waits"] = True
        m["waitList"] = [rule[0], rule[2]]
    monkeys[name] = m

figureOut = ["root"]
while figureOut:
    m = figureOut.pop(0)
    print(m)
    print(monkeys[m])
    print(figureOut)
    if monkeys[m]["waits"]:
        m1 = monkeys[m]["waitList"][0]
        m2 = monkeys[m]["waitList"][1]

        if monkeys[m1]["waits"]:
            if m1 not in figureOut:
                figureOut.append(m1)
        if monkeys[m2]["waits"]:
            if m2 not in figureOut:
                figureOut.append(m2)

        if not monkeys[m1]["waits"] and not monkeys[m2]["waits"]:
            print("finished with " + m)
            #print(monkeys[m])
            #print(monkeys[m1])
            #print(monkeys[m2])
            v = 0
            r = monkeys[m]["rule"][1]
            if isinstance(monkeys[m1]["val"], float):
                monkeys[m1]["val"] = int(monkeys[m1]["val"])
            if isinstance(monkeys[m2]["val"], float):
                monkeys[m2]["val"] = int(monkeys[m2]["val"])

            if r == "+":
                monkeys[m]["val"] = monkeys[m1]["val"] + monkeys[m2]["val"]
            elif r == "-":
                monkeys[m]["val"] = monkeys[m1]["val"] - monkeys[m2]["val"] 
            elif r == "/":
                monkeys[m]["val"] = monkeys[m1]["val"] / monkeys[m2]["val"]
            elif r == "*":
                monkeys[m]["val"] = monkeys[m1]["val"] * monkeys[m2]["val"]
            elif r == "=":
                monkeys[m]["val"] = Eq(monkeys[m1]["val"], monkeys[m2]["val"])

            if isinstance(monkeys[m]["val"], float):
                monkeys[m]["val"] = int(monkeys[m]["val"])

            monkeys[m]["waits"] = False
        elif m not in figureOut:
            figureOut.append(m)

print("==")
print(solve(monkeys["root"]["val"], dict=True))
