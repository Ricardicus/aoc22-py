from general import *
import  re

lines = readlinesFromFile("inputs/15.txt")
lines = [ line.strip() for line in lines ]

grid = []
padding = 1000000

OPEN = 1
CLOSED = 2
SENSOR = 3
BEACON = 4

"""
for i in range(1000):
    grid.append([])
    for _ in range(1000):
        grid[i].append(OPEN)
"""
def closeness(p1, p2):
    dy = abs(p1[0]-p2[0])
    dx = abs(p1[1]-p2[1])

    return dx+dy

def addToGrid(p, value):
    global grid
    grid[p[0]+padding][p[1]+padding] = value

def checkGrid(p):
    return grid[p[0]+padding][p[1]+padding]

def closeThese(point, distance):
    x = point[0]
    y = point[1]
    for dx in range(-distance, distance+1):
        for dy in range(-distance, distance+1):
            if ( abs(dx) + abs(dy) <= distance ):
                if checkGrid([x+dx,y+dy]) == OPEN:
                    addToGrid([x+dx,y+dy], CLOSED)

def closedOnRow(row):
    c = 0
    s = ""
    for i in range(len(grid[0])):
        v = grid[row+padding][i]
        if v == CLOSED:
            c += 1
            s += "#"
        elif v == OPEN:
            s += "."
        elif v == BEACON:
            s += "B"
        elif v == SENSOR:
            s += "S"
    print(s)
    return c

def gridValToChar(v):
    if v == CLOSED:
        return "#"
    elif v == OPEN:
        return "."
    elif v == BEACON:
        return "B"
    elif v == SENSOR:
        return "S"

def printGrid(ystart, yend):
    s = ""
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            s += gridValToChar(grid[x][y])
        s += "\n"
    print(s)

ints = []
for line in lines:
    print(line)
    s = line.split(" ")
    p1x = int(s[2].split("=")[1][:-1])
    p1y = int(s[3].split("=")[1][:-1])
    p2x = int(s[8].split("=")[1][:-1])
    p2y = int(s[9].split("=")[1])
    
    p1 = [p1y, p1x]
    p2 = [p2y, p2x]
    ints.append([p1x,p1y,p2x,p2y, closeness(p1,p2)])
    #addToGrid(p1, SENSOR)
    #addToGrid(p2, BEACON)
    
    #d = closeness(p1,p2)
    #closeThese(p1, d)
"""
# Part 1
c = 0
for x in range(-9019876, 9019876):
    if x % 100000 == 0:
        print(x)
    y = 2000000
    p = True
    for sx,sy,bx,by,_ in ints:
        if x == bx and y == by:
           poss = True
           break
        if closeness([sx,sy], [x,y]) <= closeness([sx,sy],[bx,by]):
           p = False
           break
    if not p:
        c += 1
print(c)
"""
limit = 4000000
for sx,sy,bx,by,d in ints:
    for dist in range(d+1):
        # Move around the edges
        for i in range(1,5):
            for mx, my in ((sx-d-i+dist, sy-dist ),
                           (sx+d+i-dist, sy-dist),
                           (sx-d-i+dist, sy+dist),
                           (sx+d+i-dist, sy+dist)):
                if 0 <= mx and mx <= limit and 0 <= my and my <= limit:
                    ok = True
                    for sxx, syy, bxx, byy, dd in ints:
                        distance_sensor = closeness([sxx, syy], [mx,my])
                        if distance_sensor < dd:
                            ok = False
                            break
                        if bxx == mx and byy == my:
                            ok = False
                            break
                    if ok:
                        print(mx*limit + my)
                        break
                    













"""





limit = 4000000
for sx,sy,bx,by,d in ints:
    for s in range(d+1):
        # Search along the outer edges
        for searchx, searchy in ((sx-d-1+s, sy-s),
                                 (sx+d+1-s, sy-s),
                                 (sx-d-1+s, sy+s),
                                 (sx+d+1-s, sy+s)):
            if ( 0 <= searchy <= limit and 0 <= searchx <= limit ):
                ok = True
                for sxx, syy, bxx, byy, dd in ints:
                    if closeness([searchx, searchy], [sxx, syy]) < dd:
                        ok = False
                if ok:
                    print(searchx * limit + searchy)
                    break


"""
