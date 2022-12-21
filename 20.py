from general import *
from copy import deepcopy

"""
lines = readlinesFromFile("inputs/20.txt")
lines = [ line.strip() for line in lines ]

file = []
idx = 0
for line in lines:
    file.append([int(line),idx])
    idx += 1


# Swap function
def movePositions(list, pos1, pos2):
    list.insert(pos2, list.pop(pos1))
    return list
 
print(file)

fileMove = deepcopy(file)
L = len(fileMove)
for number, idx in fileMove:
    print(number, idx)
    newIdx = -1
    q = 0
    for f in file:
        if f[1] == idx:
            newIdx = q
            break
        q += 1
    if newIdx >= 0:
        print("new idx for ", number, ":",newIdx)

        if number < 0:
            #if newIdx + number <= 0:
            #    q = newIdx + number
            #    while q <= 0:
            #        number -= 1
            #        q += L
            #newSpot = (newIdx+number) % L
            if newIdx + number <= 0:
                q = -(newIdx + number) + L
                times, _ = divmod(q, L)
                number -= times
            newSpot = (newIdx+number) % L
        else:
            if newIdx + number >= L:
                q = newIdx + number
                times, _ = divmod(q, L)
                number += times
            newSpot = (newIdx+number) % L
            #if newIdx + number >= L:
            #    q = newIdx + number
            #    while q >= L:
            #        number += 1
            #        q -= L
            newSpot = (newIdx+number) % L
        
        if number < 0:
            if newIdx + number <= 0:
                q = newIdx + number
                while q <= 0:
                    number -= 1
                    q += L
            newSpot = (newIdx+number) % L
        else:
            if newIdx + number >= L:
                q = newIdx + number
                while q >= L:
                    number += 1
                    q -= L
            newSpot = (newIdx+number) % L
        
        print(number, newIdx, newSpot)
        #print([f[0] for f in file])
        # Move to the right
        file = movePositions(file, newIdx, newSpot)
        #print([f[0] for f in file])

numbers = [ f[0] for f in file]
print(numbers)

def getGrove(numbers):
    zeroIdx = 0
    L = len(numbers)
    while zeroIdx < L:
        q = numbers[zeroIdx]
        if q == 0:
            break
        zeroIdx += 1
    s = 0
    for i in [1000, 2000, 3000]:
        idx = (zeroIdx + i) % L
        s += numbers[idx]
    return s

print(numbers)

print(getGrove(numbers))

import sys
sys.exit(0)
"""


lines = readlinesFromFile("inputs/20.txt")
lines = [ line.strip() for line in lines ]

key = 811589153
file = []
idx = 0
for line in lines:
    file.append([int(line)*key,idx])
    idx += 1

def movePositions(list, pos1, pos2):
    list.insert(pos2, list.pop(pos1))
    return list
 
print(file)

fileMove = deepcopy(file)
L = len(fileMove)
for _ in range(10):
    for number, idx in fileMove:
        newIdx = -1
        q = 0
        for f in file:
            if f[1] == idx:
                newIdx = q
                break
            q += 1
        v = file.pop(newIdx)
        p = (newIdx + v[0]) % (L-1)
        file.insert(p, v)

    numbers = [f[0] for f in file]
    print(numbers)
def getGrove(numbers):
    zeroIdx = 0
    L = len(numbers)
    while zeroIdx < L:
        q = numbers[zeroIdx]
        if q == 0:
            break
        zeroIdx += 1
    s = 0
    for i in [1000, 2000, 3000]:
        idx = (zeroIdx + i) % L
        s += numbers[idx]
    return s

print(numbers)
print(getGrove(numbers))
    
