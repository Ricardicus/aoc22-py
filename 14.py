from general import *
import math 
import time

lines = readlinesFromFile("inputs/14.txt")
lines = [line.strip() for line in lines]

START = 3
SAND = 2
ROCK = 1
AIR = 0

grid = []
for q in range(200):
    grid.append([])
    for i in range(600):
        grid[q].append(AIR)

start_pos = (0, 500)
grid[0][500] = START

xMax = 0
yMax = 0

def drawRock(start, end):
    global xMax
    xstart = start[1]
    ystart = start[0]
    xend = end[1]
    yend = end[0]
    xmov = int(math.copysign(1, xend-xstart))
    ymov = int(math.copysign(1, yend-ystart))
    
    if xend > xMax:
        xMax = xend

    if xstart == xend:
        # move y
        while ( ystart != yend ):
            grid[xstart][ystart] = ROCK
            ystart += ymov
        grid[xstart][ystart] = ROCK
    elif ystart == yend:
        # move x
        while ( xstart != xend ):
            grid[xstart][ystart] = ROCK
            xstart += xmov
        grid[xstart][ystart] = ROCK
def printGrid(xstart=0,xend=505):
    s = ""
    for i in range(len(grid)):
        for c in range(xstart, xend):
            if ( grid[i][c] == ROCK ):
                s += "#"
            elif ( grid[i][c] == SAND ):
                s += "o"
            elif ( grid[i][c] == START ):
                s += "+"
            else:
                s += "."
        s += "\n"
    print(s)

for line in lines:
    f = line.split(" -> ")
    r = [ int(r) for r in f[0].split(",") ]
    for ff in f[1:]:
        q = [ int(r) for r in ff.split(",") ]
        drawRock(r,q)
        r = q

class Sand:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.at_rest = False
    def move(self):
        if self._x > len(grid):
            self.at_rest = True
        if grid[self._x+1][self._y] == AIR:
            grid[self._x][self._y] = AIR
            self._x += 1
            grid[self._x][self._y] = SAND
        elif grid[self._x+1][self._y-1] == AIR:
            grid[self._x][self._y] = AIR
            self._x += 1
            self._y -= 1
            grid[self._x][self._y] = SAND
        elif grid[self._x+1][self._y+1] == AIR:
            grid[self._x][self._y] = AIR
            self._x += 1
            self._y += 1
            grid[self._x][self._y] = SAND
        else:
            self.at_rest = True

    def atRest(self):
        return self.at_rest

    def getX(self):
        return self._x

sandAtRestCount = 0

run = True
while run:
    s = Sand(start_pos[0], start_pos[1])
    while ( not s.atRest() ):
        try:
            s.move()
        except IndexError:
            run = False
            break
    sandAtRestCount += 1

print("Part 1", sandAtRestCount-1)

floor = xMax + 2
# redraw with floor

grid = []
for q in range(floor+1):
    grid.append([])
    for i in range(700):
        if q == floor:
            grid[q].append(ROCK)
        else:
            grid[q].append(AIR)

for line in lines:
    f = line.split(" -> ")
    r = [ int(r) for r in f[0].split(",") ]
    for ff in f[1:]:
        q = [ int(r) for r in ff.split(",") ]
        drawRock(r,q)
        r = q

start_pos = (0, 500)
grid[0][500] = START

sandAtRestCount = 0

run = True
while run:
    if grid[start_pos[0]][start_pos[1]] == SAND:
        run = False
        break

    s = Sand(start_pos[0], start_pos[1])
    while ( not s.atRest() ):
        try:
            s.move()
        except IndexError:

            run = False
            break
    x = s.getX()
    if ( x == 0 ):
        run = False
        sandAtRestCount += 1
        break
    sandAtRestCount += 1

print("Part 2:", sandAtRestCount)
