from general import *
import sys
import math
import time

smallPart = False
sideDim = 4
d = "inputs/22.txt"
if len(sys.argv) > 1 and sys.argv[1] == "small":
    d += ".small"
    smallPart = True
else:
    sideDim = 50 

lines = readlinesFromFile(d)
lines = [ line[:-1] if line.endswith("\n") else line for line in lines ]

grid = []
belongGrid = []
rules = []

# Types of things in the map
VOID = 0
AIR = 1
WALL = 2
EXPLORER = 3

# Find out depth / width of map
rowMax = 0
columnMax = 0
for line in lines:
    if len(line) < 2:
        break
    if len(line) > columnMax:
        columnMax = len(line)
    rowMax += 1

belongCount = 1
for i in range(rowMax):
    grid.append([])
    belongGrid.append([])
    for p in range(columnMax):
        grid[i].append(VOID)
        belongGrid[i].append(belongCount)

startPos = None
i = 0
for line in lines:
    q  = 0
    for c in line:
        if c == " ":
            pass
        elif c == ".":
            if startPos is None:
                startPos = (i, q)
            grid[i][q] = AIR
        elif c == "#":
            grid[i][q] = WALL
        q += 1
    i += 1

i = 0
belongCount = 1
startPosMap = [0,0,0,0,0,0]
for i in range(0, len(grid), sideDim):
    for q in range(0,len(grid[0]), sideDim):
        update = False
        for ii in range(sideDim):
            for qq in range(sideDim):
                if grid[i+ii][q+qq] != VOID:
                    belongGrid[i+ii][q+qq] = belongCount
                    update = True
        if update:
            startPosMap[belongCount-1] = (i,q)
            belongCount += 1
            update = False

i = 0
s = ""
for line in lines:
    q  = 0
    if len(line) < 2:
        break
    for c in line:
        if c != " ":
            s += str(belongGrid[i][q])
        else:
            s += " "
        q += 1
    s += "\n"
    i += 1

# Real directions, not as from the explorer
D_UP = 0
D_DOWN = 1
D_LEFT = 2
D_RIGHT = 3

D_map = {}
D_map[(0,1)] = D_RIGHT
D_map[(1,0)] = D_DOWN
D_map[(0,-1)] = D_LEFT
D_map[(-1, 0)] = D_UP

def getSide(pos):
    if pos[0] < 0 or pos[0] >= len(grid) or pos[1] < 0 or pos[1] >= len(grid[0]):
        return -1
    if grid[pos[0]][pos[1]] == VOID:
        return -1
    return belongGrid[pos[0]][pos[1]]

def getCoordOf(side, localPos):
    start = startPosMap[side-1]
    return [start[0] + localPos[0], start[1] + localPos[1]]

def getNextSideOutOfScopeSmall(side, direction):
    if not isinstance(direction, int):
        direction = D_map[tuple(direction)]
    if side == 1:
        if direction == D_DOWN:
            return 4
        elif direction == D_LEFT:
            return 3
        elif direction == D_RIGHT:
            return 6
        elif direction == D_UP:
            return 2
    elif side == 2:
        if direction == D_RIGHT:
            return 3
        elif direction == D_UP:
            return 1
        elif direction == D_DOWN:
            return 5
        elif direction == D_LEFT:
            return 6
    elif side == 3:
        if direction == D_LEFT:
            return 2
        elif direction == D_RIGHT:
            return 4
        elif direction == D_DOWN:
            return 5
        elif direction == D_UP:
            return 1
    elif side == 4:
        if direction == D_LEFT:
            return 3
        if direction == D_DOWN:
            return 5
        if direction == D_RIGHT:
            return 6
        if direction == D_UP:
            return 1
    elif side == 5:
        if direction == D_RIGHT:
            return 6
        if direction == D_UP:
            return 4
        if direction == D_LEFT:
            return 3
        if direction == D_DOWN:
            return 2
    elif side == 6:
        if direction == D_DOWN:
            return 2
        elif direction == D_RIGHT:
            return 1
        elif direction == D_LEFT:
            return 5
        elif direction == D_UP:
            return 4
    print("Error get next side", side ,direction)

def getNextSideOutOfScopeBig(side, direction):
    if not isinstance(direction, int):
        direction = D_map[tuple(direction)]
    if side == 1:
        if direction == D_DOWN:
            return 3
        elif direction == D_LEFT:
            return 4
        elif direction == D_RIGHT:
            return 2
        elif direction == D_UP:
            return 6
    elif side == 2:
        if direction == D_RIGHT:
            return 5
        elif direction == D_UP:
            return 6
        elif direction == D_DOWN:
            return 3
        elif direction == D_LEFT:
            return 1
    elif side == 3:
        if direction == D_LEFT:
            return 4
        elif direction == D_RIGHT:
            return 2
        elif direction == D_DOWN:
            return 5
        elif direction == D_UP:
            return 1
    elif side == 4:
        if direction == D_LEFT:
            return 1
        if direction == D_DOWN:
            return 6
        if direction == D_RIGHT:
            return 5
        if direction == D_UP:
            return 3
    elif side == 5:
        if direction == D_RIGHT:
            return 2
        if direction == D_UP:
            return 3
        if direction == D_LEFT:
            return 4
        if direction == D_DOWN:
            return 6
    elif side == 6:
        if direction == D_DOWN:
            return 2
        elif direction == D_RIGHT:
            return 5
        elif direction == D_LEFT:
            return 1
        elif direction == D_UP:
            return 4
    print("Error get next side", side ,direction)

def getLocalOf(coord):
    side = getSide(coord)
    if side == 1:
        return [coord[0], coord[1] - sideDim*2]
    elif side == 2:
        return [coord[0]-sideDim, coord[1]]
    elif side == 3:
        return [coord[0]-sideDim, coord[1]-sideDim]
    elif side == 4:
        return [coord[0]-sideDim, coord[1]-sideDim*2]
    elif side == 5:
        return [coord[0]-sideDim*2, coord[1]-sideDim*2]
    elif side == 6:
        return [coord[0]-sideDim*3, coord[1]-sideDim*3]
    else:
        print("Error!")
        sys.exit(1)

def getLocalOfBig(coord):
    side = getSide(coord)
    if side == 1:
        return [coord[0], coord[1] - sideDim]
    elif side == 2:
        return [coord[0], coord[1] - sideDim * 2]
    elif side == 3:
        return [coord[0]-sideDim, coord[1]-sideDim]
    elif side == 4:
        return [coord[0]-sideDim*2, coord[1]]
    elif side == 5:
        return [coord[0]-sideDim*2, coord[1]-sideDim]
    elif side == 6:
        return [coord[0]-sideDim*3, coord[1]]
    else:
        print("Error!")
        sys.exit(1)



# Return nextPos, nextDirection; hard coded to fit small example
def getNextPosSmall(pos, direction):
    newPosX = (pos[0] + direction[0]) 
    newPosY = (pos[1] + direction[1])
    currentSide = getSide(pos)
    if currentSide == 0:
        print("Current side is zero?")
        sys.exit(0)
    currentLocal = getLocalOf(pos)

    nextSide = getSide([newPosX, newPosY])
    if nextSide == -1:
        nextSide = getNextSideOutOfScopeSmall(currentSide, direction)

    if nextSide == currentSide:
        return [[newPosX, newPosY], direction]
    else:
        real_dir = D_map[(int(direction[0]), int(direction[1]))]
        if currentSide == 1:
            if real_dir == D_DOWN:
                return [newPosX, newPosY], direction
            if real_dir == D_LEFT:
                newLocalX = 0 
                newLocalY = currentLocal[0]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_DOWN
            if real_dir == D_RIGHT:
                newLocalX = sideDim - 1 - currentLocal[0]
                newLocalY = sideDim - 1
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_LEFT
            if real_dir == D_UP:
                newLocalX = 0
                newLocalY = sideDim - 1 - currentLocal[1]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_DOWN
        elif currentSide == 2:
            if real_dir == D_RIGHT:
                return [newPosX, newPosY], direction
            elif real_dir == D_LEFT:
                newLocalX = sideDim - 1
                newLocalY = sideDim - 1 - currentLocal[0]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_UP 
            elif real_dir == D_UP:
                newLocalX = 0
                newLocalY = sideDim - 1 - currentLocal[1]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_DOWN
            elif real_dir == D_DOWN:
                newLocalX = sideDim - 1
                newLocalY = sideDim - 1 - currentLocal[1]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_UP   
        elif currentSide == 3:
            if real_dir == D_RIGHT or real_dir == D_LEFT:
                return [newPosX, newPosY], direction
            elif real_dir == D_UP:
                newLocalX = currentLocal[1]
                newLocalY = 0
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_RIGHT
            elif real_dir == D_DOWN:
                newLocalY = 0
                newLocalX = sideDim - 1 - currentLocal[1]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_RIGHT
        elif currentSide == 4:
            if real_dir == D_UP or real_dir == D_LEFT or real_dir == D_DOWN:
                return [newPosX, newPosY], direction
            else:
                newLocalY = (sideDim - 1) - currentLocal[0]
                newLocalX = 0
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_DOWN
        elif currentSide == 5:
            if real_dir == D_RIGHT or real_dir == D_UP:
                return [newPosX, newPosY], direction
            elif real_dir == D_LEFT:
                newLocalY = (sideDim - 1) - currentLocal[0]
                newLocalX = sideDim - 1
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_UP
            elif real_dir == D_DOWN:
                newLocalY = (sideDim - 1) - currentLocal[1]
                newLocalX = sideDim - 1
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_UP
        elif currentSide == 6:
            if real_dir == D_LEFT:
                return [newPosX, newPosY], direction
            elif real_dir == D_UP:
                newLocalY = sideDim - 1
                newLocalX = sideDim - 1 - currentLocal[1]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_LEFT
            elif real_dir == D_DOWN:
                newLocalY = 0 
                newLocalX = sideDim - 1 - currentLocal[1]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_RIGHT
            elif real_dir == D_RIGHT:
                newLocalY = 0 
                newLocalX = sideDim - 1 - currentLocal[0]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_LEFT
        else:
            print("Invalid side: ", side)
            sys.exit(1)

    print("Error", pos, currentSide, currentLocal, direction)
    sys.exit(1)

# Return nextPos, nextDirection; hard coded to fit small example
def getNextPosBig(pos, direction):
    newPosX = (pos[0] + direction[0]) 
    newPosY = (pos[1] + direction[1])
    currentSide = getSide(pos)
    if currentSide == 0:
        print("Current side is zero?")
        sys.exit(0)
    currentLocal = getLocalOfBig(pos)

    nextSide = getSide([newPosX, newPosY])
    if nextSide == -1:
        nextSide = getNextSideOutOfScopeBig(currentSide, direction)

    if nextSide == currentSide:
        return [[newPosX, newPosY], direction]
    else:
        real_dir = D_map[(int(direction[0]), int(direction[1]))]
        if currentSide == 1:
            if real_dir == D_DOWN or real_dir == D_RIGHT:
                return [newPosX, newPosY], direction
            if real_dir == D_LEFT:
                newLocalX = sideDim - 1 - currentLocal[0] 
                newLocalY = 0
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_RIGHT
            if real_dir == D_UP:
                newLocalX = currentLocal[1]
                newLocalY = 0
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_RIGHT

        elif currentSide == 2:
            if real_dir == D_LEFT:
                return [newPosX, newPosY], direction
            elif real_dir == D_RIGHT:
                newLocalX = sideDim - 1 - currentLocal[0]
                newLocalY = sideDim - 1
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_LEFT 
            elif real_dir == D_UP:
                newLocalX = sideDim - 1
                newLocalY = currentLocal[1]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_UP
            elif real_dir == D_DOWN:
                newLocalX = currentLocal[1]
                newLocalY = sideDim - 1
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_LEFT  
            
        elif currentSide == 3:
            if real_dir == D_UP or real_dir == D_DOWN:
                return [newPosX, newPosY], direction
            elif real_dir == D_LEFT:
                newLocalX = 0
                newLocalY = currentLocal[0]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_DOWN
            elif real_dir == D_RIGHT:
                newLocalY = currentLocal[0]
                newLocalX = sideDim - 1
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_UP

        elif currentSide == 4:
            if real_dir == D_RIGHT or real_dir == D_DOWN:
                return [newPosX, newPosY], direction
            elif real_dir == D_UP:
                newLocalY = 0
                newLocalX = currentLocal[1]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_RIGHT
            elif real_dir == D_LEFT:
                newLocalY = 0
                newLocalX = sideDim - 1 - currentLocal[0]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_RIGHT

        elif currentSide == 5:
            if real_dir == D_UP or real_dir == D_LEFT:
                return [newPosX, newPosY], direction
            elif real_dir == D_RIGHT:
                newLocalY = sideDim - 1
                newLocalX = sideDim - 1 - currentLocal[0]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_LEFT
            elif real_dir == D_DOWN:
                newLocalY = sideDim - 1
                newLocalX = currentLocal[1]
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_LEFT

        elif currentSide == 6:
            if real_dir == D_UP:
                return [newPosX, newPosY], direction
            elif real_dir == D_RIGHT:
                newLocalY = currentLocal[0]
                newLocalX = sideDim - 1
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_UP
            elif real_dir == D_LEFT:
                newLocalY = currentLocal[0] 
                newLocalX = 0
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_DOWN
            elif real_dir == D_DOWN:
                newLocalY = currentLocal[1] 
                newLocalX = 0
                newPos = getCoordOf(nextSide,[newLocalX, newLocalY])
                return newPos, D_DOWN
        else:
            print("Invalid side: ", side)
            sys.exit(1)

    print("Error", pos, currentSide, currentLocal, direction)
    sys.exit(1)

LEFT = -2
RIGHT = -3
# Parse rules
rules = lines[-1]
r = rules.split("R")
rr = " ".join(r)
tt = " ".join(rr.split("L"))
tt = [ int(x) for x in tt.split(" ") ]
q = 0
rulz = []
addedNumeric = False
addedNumericCount = 0
while q < len(rules):
    if not addedNumeric and rules[q].isnumeric():
        rulz.append(tt[addedNumericCount])
        addedNumericCount += 1
        addedNumeric = True
    if rules[q] == "R":
        rulz.append(RIGHT)
        addedNumeric = False
    elif rules[q] == "L":
        rulz.append(LEFT)
        addedNumeric = False

    q += 1
print(rulz)

def displayGrid():
    s = ""
    for i in range(len(grid)):
        for n in range(len(grid[0])):
            if grid[i][n] == VOID:
                s += " "
            elif grid[i][n] == AIR:
                s += "."
            elif grid[i][n] == WALL:
                s += "#"
            elif grid[i][n] == EXPLORER:
                s += "E"
        s += "\n"
    print(s)

displayGrid()

class Explorer:
    def __init__(self, startx, starty, rules):
        self.x = startx
        self.y = starty
        self.omega = 90
        self.rules = rules
        self.reachedTarget = False
        self.index = 0
        self.trail = []
    
    def setAngleAccordingToDirection(self, direction):
        if not isinstance(direction, int):
            direction = D_map[tuple(direction)]
        if direction == D_RIGHT:
            self.omega = 90
        elif direction == D_LEFT:
            self.omega = 270
        elif direction == D_UP:
            self.omega = 180
        elif direction == D_DOWN:
            self.omega = 0
        else:
            print("Error setting angle to", direction)
            sys.exit(1)

    def hasStopped(self):
        return self.reachedTarget

    def getDirection(self):
        self.omega = self.omega % 360
        if self.omega == 90:
            # Right
            return 0
        if self.omega == 180:
            # Up
            return 3
        if self.omega == 0:
            # down
            return 1
        else:
            # left
            return 2
        return self.omega

    def getPos(self):
        return [self.x, self.y]

    def update(self):
        if self.reachedTarget:
            return

        r = self.rules[self.index]

        if r == RIGHT:
            self.omega -= 90
        elif r == LEFT:
            self.omega += 90
        else:
            for _ in range(r):
                dx = round(math.cos(math.radians(self.omega)))
                dy = round(math.sin(math.radians(self.omega)))
        
                currentPos = [self.x, self.y]
                currentDir = [int(dx), int(dy)]

                if smallPart:
                    nextPos, nextDir = getNextPosSmall(currentPos, currentDir)
                else:
                    nextPos, nextDir = getNextPosBig(currentPos, currentDir)

                # Check if collision
                if grid[nextPos[0]][nextPos[1]] == WALL:
                    # don't move 
                    #self.draw()
                    #displayGrid()
                    #self.clear()
                    break
                else:
                    self.setAngleAccordingToDirection(nextDir)
                    self.x, self.y = nextPos

                #self.draw()
                #displayGrid()
                #time.sleep(1)
                #self.clear()

        self.index += 1
        if self.index == len(self.rules):
            self.reachedTarget = True

    def draw(self):
        grid[self.x][self.y] = EXPLORER

    def clear(self):
        grid[self.x][self.y] = AIR

e = Explorer(startPos[0], startPos[1], rulz)

while not e.hasStopped():
    #e.draw()
    #displayGrid()
    #time.sleep(0.1)
    #e.clear()

    e.update()
e.draw()
displayGrid()

pos = e.getPos()
dr = e.getDirection()

count = (pos[0]+1) * 1000 + (pos[1]+1)*4 + dr
print(count)
