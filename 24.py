from general import *
import sys
import time
import random
from copy import deepcopy
import hashlib
from collections import deque


# Will try to solve this with random explore,
# heuristic: down if can else right, else wait, else left, else up

d = "inputs/24.txt"
partTwo = False
if len(sys.argv) > 1 and sys.argv[1] == "small":
    d += ".small"
if len(sys.argv) > 1 and sys.argv[1] == "2":
    partTwo = True

lines = readlinesFromFile(d)
lines = [ line[:-1] if line.endswith("\n") else line for line in lines ]

# Rounds 
rounds = 10

# Directions
UP = (-1,0)
DOWN = (1,0)
LEFT = (0,-1)
RIGHT = (0,1)

D_display = {}
D_display[UP] = "^"
D_display[DOWN] = "v"
D_display[LEFT] = "<"
D_display[RIGHT] = ">"

#NORTH_CHECK = [(-1,0),(-1,-1),(-1,1)]
#SOUTH_CHECK = [(1,0),(1,-1),(1,1)]
#WEST_CHECK = [(0,-1),(1,-1),(-1,-1)]
#EAST_CHECK = [(0,1),(-1,1),(1,1)]
#ELVE_CHECK_LIST = [NORTH_CHECK, SOUTH_CHECK, WEST_CHECK, EAST_CHECK]

# Grid values
EMPTY = 0
WALL = 1
EXPEDITION = 2
BLIZZARD = 3

# Building the grid
PADDING = 0
#if partTwo:
#    PADDING = 100

# The grid
grid = []

class Blizzard:
    def __init__(self, startx, starty, direction):
        self.x = startx
        self.y = starty
        self.direction = direction
        self.startx = startx
        self.starty = starty

    def reset(self):
        self.x = self.startx
        self.y = self.starty

    def get_next_pos(self):
        newX = self.x + self.direction[0]
        newY = self.y + self.direction[1]

        if grid[newX][newY] == WALL:
            # Wrap around, "conservation of energy"
            if newX == 0:
                newX = len(grid) - 2
            if newX == len(grid) - 1:
                newX = 1
            if newY == 0:
                newY = len(grid[0]) - 2
            if newY == len(grid[0]) - 1:
                newY = 1
        return tuple([newX, newY])
    
    def update(self):
        newX, newY = self.get_next_pos()
        self.x = newX
        self.y = newY

    def draw(self):
        v = D_display[self.direction]
        if isinstance(grid[self.x][self.y], str):
            grid[self.x][self.y] = BLIZZARD + 1
        elif grid[self.x][self.y] >= BLIZZARD:
            grid[self.x][self.y] += 1
        elif grid[self.x][self.y] == EMPTY:
            grid[self.x][self.y] = v

    def clear(self):
        grid[self.x][self.y] = EMPTY

blizzards = []
i = 0
for line in lines:
    grid.append([])
    q = 0
    for c in line:
        if c == ".":
            grid[i].append(EMPTY)
        elif c == "#":
            grid[i].append(WALL)
        elif c == "<":
            grid[i].append(BLIZZARD)
            blizzards.append(Blizzard(i, q, LEFT))
        elif c == ">":
            grid[i].append(BLIZZARD)
            blizzards.append(Blizzard(i, q, RIGHT))
        elif c == "^":
            grid[i].append(BLIZZARD)
            blizzards.append(Blizzard(i, q, UP))
        elif c == "v":
            grid[i].append(BLIZZARD)
            blizzards.append(Blizzard(i, q, DOWN))
        q += 1
    i += 1

for blizzard in blizzards:
    blizzard.clear()

def displayGrid(upto=1000):
    s = ""
    for i in range(upto):
        if i >= len(grid):
            break
        for q in range(upto):
            if q >= len(grid[0]):
                break
            if grid[i][q] == EMPTY:
                s += "."
            elif grid[i][q] == WALL:
                s += "#"
            elif grid[i][q] == EXPEDITION:
                s += "E"
            elif isinstance(grid[i][q], str):
                s += grid[i][q]
            elif grid[i][q] >= BLIZZARD:
                s += str(grid[i][q]-2)

        s += "\n"
    print(s)

def displayGivenGrid(grid, x=0, y=1, upto=1000):
    s = ""
    for i in range(upto):
        if i >= len(grid):
            break
        for q in range(upto):
            if q >= len(grid[0]):
                break
            if i == x and q == y:
                if grid[i][q] == EMPTY:
                    s += "E"
                else:
                    s += "!"
            elif grid[i][q] == EMPTY:
                s += "."
            elif grid[i][q] == WALL:
                s += "#"
            elif grid[i][q] == EXPEDITION:
                s += "E"
            elif isinstance(grid[i][q], str):
                s += grid[i][q]
            elif grid[i][q] >= BLIZZARD:
                s += str(grid[i][q]-2)

        s += "\n"
    print(s)



def gridHash(upto=1000):
    s = ""
    for i in range(upto):
        if i >= len(grid):
            break
        for q in range(upto):
            if q >= len(grid[0]):
                break
            if grid[i][q] == EMPTY:
                s += "."
            elif grid[i][q] == WALL:
                s += "#"
            elif grid[i][q] == EXPEDITION:
                s += "E"
            elif isinstance(grid[i][q], str):
                s += grid[i][q]
            elif grid[i][q] >= BLIZZARD:
                s += str(grid[i][q]-2)

        s += "\n"
    result = hashlib.sha256(s.encode())
    return result.hexdigest()

def updateBlizzards():
    for b in blizzards:
        b.clear()
    for b in blizzards:
        b.update()
    for b in blizzards:
        b.draw()

def resetBlizzards():
    for b in blizzards:
        b.clear()
    for b in blizzards:
        b.reset()
    for b in blizzards:
        b.draw()

# Check when the map repeats
hashes = set()
resetBlizzards()
indexCount = 0
while True:
    updateBlizzards()
    h = gridHash()
    if h in hashes:
        break
    hashes.add(h) 
    indexCount += 1
print("Map repeats after",indexCount,"steps")
resetBlizzards()
timeGrids = []
i = 0
while i < indexCount:
    timeGrids.append(deepcopy(grid))
    updateBlizzards()
    i += 1
timeLoop = indexCount
displayGivenGrid(timeGrids[0])
displayGivenGrid(timeGrids[1])
displayGivenGrid(timeGrids[-1])

WAIT = 0
MOVE_LEFT = 1
MOVE_RIGHT = 2
MOVE_UP = 3
MOVE_DOWN = 4 

# Part 1
# Do a BFS search, state: time, pos
seen = set()
state = (0, (0, 1))
states = []
states.append(state)
minTime = 999999
maxY = 0
maxX = 0

while states:
    t, pos = states.pop(0)
    
    #print(time, pos, minTime, states)
    
    if t > minTime:
        continue
    if pos[0] == len(grid) - 1 and pos[1] == len(grid[0]) - 2:
        if t < minTime:
            minTime = t
            print("Found home, new time:",t)

    # Check possibilities
    for d in [(0,0), (-1,0), (1, 0), (0, 1), (0, -1)]:
        nx = pos[0] + d[0]
        ny = pos[1] + d[1]
        newState = ((t+1), (nx, ny))
        newSeenState = ((t+1)%timeLoop, (nx,ny))

        if nx < 0 or nx > len(grid) - 1:
            continue
        if ny < 0 or ny >= len(grid[0]) - 1:
            continue
        if timeGrids[newSeenState[0]][nx][ny] != EMPTY:
            #print(timeGrids[(time+1)%timeLoop][nx][ny])
            continue
        elif newSeenState in seen:
            continue

        #print(newState)
        #displayGivenGrid(timeGrids[newSeenState[0]], nx, ny)
        #time.sleep(1)
        seen.add(newSeenState)
        states.append(newState)

print(minTime)
# Part 2
# Do a BFS search, state: time, pos. Do it 3 times, dont reset time state
# Start from previous end
seen = set()
state = (minTime, (len(grid)-1, len(grid[0])-2))
states = []
states.append(state)
minTime = 999999
maxY = 0
maxX = 0
timeIndexStart = minTime

while states:
    t, pos = states.pop(0)
    
    #print(time, pos, minTime, states)
    
    if t > minTime:
        continue

    if pos[0] == 0 and pos[1] == 1:
        # Reached back!
        if t < minTime:
            minTime = t
            print("new min time:", minTime)

    # Check possibilities
    for d in [(0,0), (-1,0), (1, 0), (0, 1), (0, -1)]:
        nx = pos[0] + d[0]
        ny = pos[1] + d[1]
        newState = ((t+1), (nx, ny) )
        newSeenState = ((t+1)%timeLoop, (nx,ny))

        if nx < 0 or nx > len(grid) - 1:
            continue
        if ny < 0 or ny >= len(grid[0]) - 1:
            continue
        if timeGrids[newSeenState[0]][nx][ny] != EMPTY:
            #print(timeGrids[(time+1)%timeLoop][nx][ny])
            continue
        elif newSeenState in seen:
            continue
        #print(newState)
        #displayGivenGrid(timeGrids[newSeenState[0]], nx, ny)
        #time.sleep(1)
        seen.add(newSeenState)
        states.append(newState)

seen = set()
state = (minTime, (0, 1))
states = []
states.append(state)
minTime = 999999
maxY = 0
maxX = 0
timeIndexStart = minTime

while states:
    t, pos = states.pop(0)
    
    #print(time, pos, minTime, states)
    
    if t > minTime:
        continue
    if pos[0] == len(grid) - 1 and pos[1] == len(grid[0]) - 2:
        if t < minTime:
            minTime = t
            print("Found home, new time:",t)

    # Check possibilities
    for d in [(0,0), (-1,0), (1, 0), (0, 1), (0, -1)]:
        nx = pos[0] + d[0]
        ny = pos[1] + d[1]
        newState = ((t+1), (nx, ny) )
        newSeenState = ((t+1)%timeLoop, (nx,ny))

        if nx < 0 or nx > len(grid) - 1:
            continue
        if ny < 0 or ny >= len(grid[0]) - 1:
            continue
        if timeGrids[newSeenState[0]][nx][ny] != EMPTY:
            #print(timeGrids[(time+1)%timeLoop][nx][ny])
            continue
        elif newSeenState in seen:
            continue
        #print(newState)
        #displayGivenGrid(timeGrids[newSeenState[0]], nx, ny)
        #time.sleep(1)
        seen.add(newSeenState)
        states.append(newState)


print("Found goal twice, min time:", minTime)
print(minTime)
