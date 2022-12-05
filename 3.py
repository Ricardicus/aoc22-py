from general import *

def prioPoint(a):
    if ord(a) >= ord("a") and ord(a) <= ord("z"):
        return (1+ord(a)-ord("a"))
    elif ord(a) >= ord("A") and ord(a) <= ord("Z"):
        return  (ord(a)+1-ord("A")+26)
    raise ValueError("NO:" + a)

lines = readlinesFromFile("inputs/3.txt")
count = 0
for line in lines:
    line = line.strip()
    l = int(len(line)/2)
    p1 = line[:l]
    p2 = line[l:]
    for c in p1:
        if c in p2:
            count += prioPoint(c)
            break

print("Part 1:", count)

def findCommonItem(l1,l2,l3):
    ccount = {}
    lcombi = l1.strip()+l2.strip()+l3.strip()
    for c in lcombi:
        if c in ccount:
            ccount[c] += 1
        else:
            ccount[c] = 1
    interesting = []
    for k in ccount:
        if ccount[k] >= 3:
            interesting.append(k)
    for i in interesting:
        if i in l1 and i in l2 and i in l3:
            return i
    raise ValueError("No common")

i = 0
count = 0
while ( i < len(lines) ):
    c = findCommonItem(lines[i], lines[i+1], lines[i+2])
    count += prioPoint(c)
    i += 3

print("Part 2:", count)
