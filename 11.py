from general import *
from functools import reduce

lines = readlinesFromFile("inputs/11.txt")

monkas = []

i = 0
while ( i < len(lines) ):
    line = lines[i].strip()
    if ( line.startswith("Monkey") ):
        newMonka = {}
        newMonka["si"] = [ int(x) for x in lines[i+1].split(":")[1].strip().split(",") ]
        newMonka["op"] = lines[i+2].split("=")[1].strip().split(" ")
        newMonka["test"] = int(lines[i+3].split("divisible by")[1].strip())
        newMonka["ttrue"] = int(lines[i+4].split("monkey")[1].strip())
        newMonka["tfalse"] = int(lines[i+5].split("monkey")[1].strip())
        newMonka["inspects"] = 0
        monkas.append(newMonka)
    i += 1

monkas_orig = monkas.copy()

modulus = reduce((lambda x, y: x*y), [ m["test"] for m in monkas ])

partOne = True
def performRound():
    q = 0
    while ( q < len(monkas) ):
        m = monkas[q]
        l = m["si"]
        while ( len(l) > 0 ):
            i = l.pop(0)
            newV = i
            v = m["op"][2]
            if ( v == "old" ):
                v = i
            else:
                v = int(v)
            if m["op"][1] == "+":
                newV += v
            elif m["op"][1] == "*":
                newV *= v
            if partOne:
                newV = int(newV/3)
            else:
                newV = newV % modulus
            monkas[q]["inspects"] += 1
            testV = m["test"]
            if newV % testV == 0:
                monkas[m["ttrue"]]["si"].append(newV)
            else:
                monkas[m["tfalse"]]["si"].append(newV)
        q += 1

print(monkas)
"""
rounds = 20
for _ in range(rounds):
    performRound()

inspects = []
for m in monkas:
    inspects.append(m["inspects"])
print(monkas)
inspects.sort(reverse=True)
print(inspects[0]*inspects[1])

"""
partOne = False
monkas = monkas_orig

rounds = 10000
for r in range(rounds):
    performRound()
    print(r)

inspects = []
for m in monkas:
    inspects.append(m["inspects"])
print(monkas)
inspects.sort(reverse=True)
print(inspects[0]*inspects[1])
