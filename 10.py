from general import *

lines = readlinesFromFile("inputs/10.txt")
lines = [ line.strip() for line in lines ]


X = 1
cycle = 0

sigStrenSum = 0
def cycleValueChecker():
    global sigStrenSum
    if cycle == 20 or cycle == 60 or cycle == 100 or cycle == 140 or cycle == 180 or cycle == 220:
        sigStrenSum += cycle * X

def cyclePrint():
    c = X
    d = cycle % 40
    if d <= c + 2 and d >= c:
        print("#",end="")
    else:
        print(".",end="")
    if ( cycle % 40 == 0):
        print("\n", end="")

for line in lines:
    if line.startswith("noop"):
        cycle += 1
        cycleValueChecker()
    if line.startswith("addx"):
        v = int(line.split(" ")[1])
        cycle += 1
        cycleValueChecker()
        cycle += 1
        cycleValueChecker()
        X += v

print(sigStrenSum)

cycle = 0
X=1
for line in lines:
    if line.startswith("noop"):
        cycle += 1
        cycleValueChecker()
    if line.startswith("addx"):
        v = int(line.split(" ")[1])
        cycle += 1
        cycleValueChecker()
        cycle += 1
        cycleValueChecker()
        X += v

print(sigStrenSum)
cycle = 0
X = 1
for line in lines:
    if line.startswith("noop"):
        cycle += 1
        cyclePrint()
    if line.startswith("addx"):
        v = int(line.split(" ")[1])
        cycle += 1
        cyclePrint()
        cycle += 1
        cyclePrint()
        X += v



