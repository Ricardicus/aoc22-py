from general import *
import sys
import time

d = "inputs/23.txt"
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
NORTH = (-1,0)
SOUTH = (1,0)
WEST = (0,-1)
EAST = (0,1)

NORTH_CHECK = [(-1,0),(-1,-1),(-1,1)]
SOUTH_CHECK = [(1,0),(1,-1),(1,1)]
WEST_CHECK = [(0,-1),(1,-1),(-1,-1)]
EAST_CHECK = [(0,1),(-1,1),(1,1)]
ELVE_CHECK_LIST = [NORTH_CHECK, SOUTH_CHECK, WEST_CHECK, EAST_CHECK]

# Grid values
EMPTY = 0
ELVE = 1
ELVE_PROPOSE = 2

# Building the grid
PADDING = 20
if partTwo:
    PADDING = 100

grid = []
i = 0
for i in range(int(PADDING/2)):
    grid.append([])
    for _ in range(len(lines[0])+PADDING):
        grid[i].append(EMPTY)
l = len(grid)
i = 0
for line in lines:
    grid.append([])
    for _ in range(int(PADDING/2)):
        grid[l+i].append(EMPTY)
    q = 0
    for c in line:
        if c == ".":
            grid[l+i].append(EMPTY)
        elif c == "#":
            grid[l+i].append(ELVE)
        q += 1
    for _ in range(int(PADDING/2)):
        grid[l+i].append(EMPTY)
    i += 1
l = len(grid)
for i in range(int(PADDING/2)):
    grid.append([])
    for _ in range(len(lines[0]) + PADDING):
        grid[l+i].append(EMPTY)

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
            elif grid[i][q] == ELVE:
                s += "#"
        s += "\n"
    print(s)

#displayGrid()
#sys.exit(0)

def removeProposed():
    for i in range(len(grid)):
        for q in range(len(grid[0])):
            if grid[i][q] >= ELVE_PROPOSE:
                grid[i][q] = EMPTY

def countInRegion(elves):
    minX, maxX = 100000, 0
    minY, maxY = 100000, 0
    for e in elves:
        x, y = e.getPos()
        if x > maxX:
            maxX = x
        if x < minX:
            minX = x
        if y > maxY:
            maxY = y
        if y < minY:
            minY = y
    count = 0
    for x in range(minX, maxX+1):
        for y in range(minY, maxY+1):
            if grid[x][y] == EMPTY:
                count += 1
    return count

class Elve:
    def __init__(self, startX, startY):
        self.x = startX
        self.y = startY
        self.tick = 0
        self.hasProposed = False
        self.proposed = [0,0]
        self.hasMoved = False

    def clear(self):
        grid[self.x][self.y] = EMPTY

    def draw(self):
        grid[self.x][self.y] = ELVE

    def getPos(self):
        return [self.x, self.y]

    # Check if it is empty
    def checkIfElve(self, pos):
        if 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0]):
            if grid[pos[0]][pos[1]] == ELVE:
                return True
        return False

    def checkInGrid(self, pos):
        if 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0]):
            return True
        return False

    # Check if it is empty
    def checkIfProposed(self, pos):
        if 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0]):
            if grid[pos[0]][pos[1]] >= ELVE_PROPOSE:
                return True
        return False

    def move(self):
        if self.hasProposed:
            if grid[self.proposed[0]][self.proposed[1]] == ELVE_PROPOSE:
                self.x = self.proposed[0]
                self.y = self.proposed[1]
                self.hasMoved = True
            else:
                self.hasMoved = False
        # Update tick
        self.tick += 1

    def didMove(self):
        return self.hasMoved

    def propose(self):
        # Check if we need to move, first half
        elveCount = 0
        self.hasMoved = False
        for pos in [(1,0), (1,1), (1, -1), (0,1),(0,-1),(-1,-1), (-1,1),(-1,0)]:
            pos = (self.x + pos[0], self.y + pos[1])
            if self.checkInGrid(pos) and self.checkIfElve(pos):
                elveCount += 1
        if elveCount == 0:
            # Don't propose a move
            self.hasProposed = False
        else:
            # Propose a position
            checkIndex = self.tick
            checkCount = 0
            foundValid = False
            toPropose = [0,0]
            while checkCount < 4 and not foundValid:
                checks = ELVE_CHECK_LIST[checkIndex % len(ELVE_CHECK_LIST)]
                passed = True
                for pos in checks:
                    pos = [self.x + pos[0], self.y + pos[1]]
                    if self.checkInGrid(pos) and self.checkIfElve(pos):
                        passed = False
                if passed:
                    toPropose = (self.x + checks[0][0], self.y + checks[0][1])
                    foundValid = True

                checkIndex += 1
                checkCount += 1

            if foundValid:
                # Propose the position
                v = grid[toPropose[0]][toPropose[1]]
                if v == EMPTY:
                    grid[toPropose[0]][toPropose[1]] = ELVE_PROPOSE
                elif v >= ELVE_PROPOSE:
                    grid[toPropose[0]][toPropose[1]] += 1

                self.hasProposed = True
                self.proposed = toPropose
            else:
                self.hasProposed = False

elves = []
for i in range(len(grid)):
    for q in range(len(grid[0])):
        if grid[i][q] == ELVE:
            e = Elve(i, q)
            elves.append(e)
            grid[i][q] = EMPTY

displayGrid()
for e in elves:
    e.clear()
displayGrid()
for e in elves:
    e.draw()
displayGrid()

if not partTwo:
    for roundCount in range(rounds):

        # Propose step
        for e in elves:
            e.propose()
        
        # Clear
        for e in elves:
            e.clear()

        # Move step
        for e in elves:
            e.move()

        for e in elves:
            e.draw()
        
        removeProposed()
        #print("Round", roundCount+1)
        #displayGrid()
        #time.sleep(0.5)

    print(countInRegion(elves))
else:
    roundCount = 0
    someMoved = True
    while someMoved:

        # Propose step
        for e in elves:
            e.propose()
        
        # Clear
        for e in elves:
            e.clear()

        # Move step
        for e in elves:
            e.move()

        for e in elves:
            e.draw()

        # How many moved?
        movedCount = 0
        for e in elves:
            if e.didMove():
                movedCount += 1
        if movedCount == 0:
            someMoved = False
        
        removeProposed()
        print("Round", roundCount+1, ", moved:" , movedCount, " (", len(elves), ")")
        #displayGrid(20)
        #time.sleep(0.5)
        roundCount += 1
    print("Part 2:", roundCount)
