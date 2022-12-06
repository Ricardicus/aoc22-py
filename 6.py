from general import *

lines = readlinesFromFile("inputs/6.txt")

stream = lines[0]

index = 4 
start_marker =[ x for x in stream[:4] ]

def all_unique(p):
    count = {}
    for c in p:
        if c in count:
            return False
        count[c] = 1
    return True

for c in stream[4:]:
    if all_unique(start_marker):
        print("Part 1:", index)
        break
    start_marker.pop(0)
    start_marker.append(c)
    index += 1

start_marker =[ x for x in stream[:14] ]
index = 14

def all_unique(p):
    count = {}
    for c in p:
        if c in count:
            return False
        count[c] = 1
    return True

for c in stream[14:]:
    if all_unique(start_marker):
        print("Part 2:", index) 
        break
    start_marker.pop(0)
    start_marker.append(c)
    index += 1
