from general import *

lines = readlinesFromFile("inputs/12.txt")
lines = [ line.strip() for line in lines ]

grid = []
for i in range(len(lines)):
    global start
    global end
    grid.append([])
    for n in range(len(lines[0])):
        v = lines[i][n]
        if ( v == "S" ):
            start = [i,n]
            print("Start" , start)
            v = "a"
        if ( v == "E" ):
            end = [i, n]
            v = "z"
            print("end", end)
        grid[i].append(ord(v))


def pos2Key(pos):
    return str(pos[0]) + "," + str(pos[1])
def getMoves(pos):
    # move in either up or the same elevation
    x, y = pos
    valid = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            if abs(dx) + abs(dy) == 2:
                continue
            p1 = x + dx
            p2 = y + dy
            if p1 < 0 or p1 >= len(grid):
                continue
            if p2 < 0 or p2 >= len(grid[0]):
                continue
            k = str(p1) + "," + str(p2)
            if (grid[p1][p2] == grid[x][y] or grid[p1][p2] == grid[x][y]+1):
                valid.append([p1, p2])
    return valid

pos = start
queue = [((start[0], start[1]), 0)]

visited = set()
while ( len(queue) > 0 ):
    (x, y), le = queue.pop(0)
    k = pos2Key((x,y))
    if x == end[0] and y == end[1]:
        print("Part 1:", le, ", ", x, ",", y)
        break
    if k in visited:
        continue
    visited.add(k)
    for dx,dy in [(-1, 0),(0,1),(1,0),(0,-1)]:
        xx = x+dx
        yy = y+dy
        if 0 <= xx < len(grid) and 0 <= yy < len(grid[0]) and (grid[xx][yy] <= 1 + grid[x][y]):
            queue.append(((xx,yy),le+1))

visited = set()
queue = []
for i in range(0, len(grid)):
    for n in range(0, len(grid[0])):
        if chr(grid[i][n]) == "a":
            queue.append(((i,n), 0))
while ( len(queue) > 0 ):
    (x, y), le = queue.pop(0)
    k = pos2Key((x,y))
    if x == end[0] and y == end[1]:
        print("Part 2:", le, ", ", x, ",", y)
        break
    if k in visited:
        continue
    visited.add(k)
    for dx,dy in [(-1, 0),(0,1),(1,0),(0,-1)]:
        xx = x+dx
        yy = y+dy
        if 0 <= xx < len(grid) and 0 <= yy < len(grid[0]) and (grid[xx][yy] <= 1 + grid[x][y]):
            queue.append(((xx,yy),le+1))


