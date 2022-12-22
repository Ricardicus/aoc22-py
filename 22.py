from general import *
import sys
import math
import time

d = "inputs/22.txt"
if len(sys.argv) > 1 and sys.argv[1] == "small":
    d += ".small"

lines = readlinesFromFile(d)
lines = [ line[:-1] if line.endswith("\n") else line for line in lines ]

grid = []
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

for i in range(rowMax):
    grid.append([])
    for p in range(columnMax):
        grid[i].append(VOID)

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

LEFT = -2
RIGHT = -3
# Parse rules
rules = lines[-1]
print(rules)
r = rules.split("R")
rr = " ".join(r)
tt = " ".join(rr.split("L"))
tt = [ int(x) for x in tt.split(" ") ]
print(tt)
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
        print("YEAH") 
        return self.omega

    def getPos(self):
        return [self.x, self.y]

    def update(self):
        if self.reachedTarget:
            return

        r = self.rules[self.index]

        dx = round(math.cos(math.radians(self.omega)))
        dy = round(math.sin(math.radians(self.omega)))
        
        if r == RIGHT:
            self.omega -= 90
        elif r == LEFT:
            self.omega += 90
        else:
            for p in range(r):
                checkX = (self.x + dx) % rowMax
                checkY = (self.y + dy) % columnMax

                if grid[checkX][checkY] == WALL:
                    # Don't continue
                    print("WALL!")
                    break
                elif grid[checkX][checkY] == VOID:
                    # Find width of OK'ness
                    q = 0
                    testOmega = self.omega + 180
                    width = 0
                    while q < rowMax*columnMax:
                        fx = self.x
                        fy = self.y
                        dfx = round(math.cos(math.radians(testOmega)))
                        dfy = round(math.sin(math.radians(testOmega)))

                        ffx = fx + dfx * q
                        ffy = fy + dfy * q
                        if ffx >= 0 and ffx < rowMax and ffy >= 0 and ffy < columnMax:
                            if grid[ffx][ffy] != VOID:
                                width += 1
                            else:
                                break
                        q += 1
                    print("Width in direction:", width)
                    px = self.x
                    py = self.y
                    if abs(dx) == 1:
                        # moving vertically
                        px = self.x - dx * (width-1)
                        print("vertical", px, self.x)
                    if abs(dy) == 1:
                        # moving vertically
                        py = self.y - dy * (width-1)
                        print("horizontal", py, self.y)
                    if grid[px][py] == WALL:
                        # Don't continue
                        print("Wall here!")
                        break

                    # Found it
                    #self.clear()
                    print("Set to wrap",px,py)
                    self.x = px
                    self.y = py
                    self.trail.append([px, py])
                    #self.draw()
                    #displayGrid()
                    #time.sleep(1)
                elif grid[checkX][checkY] == AIR:
                    #self.clear()
                    self.x = checkX
                    self.y = checkY
                    print("Set to check", self.x, self.y)
                    #self.draw()
                    #displayGrid()
                    #time.sleep(1)
                    self.trail.append([checkX, checkY])

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
    #time.sleep(1)
    #e.clear()

    e.update()

pos = e.getPos()
dr = e.getDirection()

print(pos)
print(dr)
count = (pos[0]+1) * 1000 + (pos[1]+1)*4 + dr
print(count)
