from general import *

lines = readlinesFromFile("inputs/8.txt")
lines = [ l.strip() for l in lines ]
grid = []
i = 0
for line in lines:
    grid.append([])
    for l in line:
        grid[i].append(int(l))
    i += 1

visible = len(grid)*2 + len(grid[0])*2-4
for x in range(1, len(grid)-1):
    for y in range(1, len(grid[0])-1):
        v = grid[x][y]
        xx = x-1
        # Check up
        m = 0
        while ( xx >= 0 ):
            vv = grid[xx][y]
            if ( vv > m ):
                m = vv
            xx -= 1
        if ( m < v ):
            visible += 1
            continue
        xx = x+1
        # Check down
        m = 0
        while ( xx < len(grid) ):
            vv = grid[xx][y]
            if ( vv > m ):
                m = vv
            xx += 1
        if ( m < v ):
            visible += 1
            continue
        # Check left
        m = 0
        yy = y-1
        while ( yy >= 0 ):
            vv = grid[x][yy]
            if ( vv > m ):
                m = vv
            yy -= 1
        if ( m < v ):
            visible += 1
            continue
        # Check right
        m = 0
        yy = y+1
        while ( yy < len(grid[0]) ):
            vv = grid[x][yy]
            if ( vv > m ):
                m = vv
            yy += 1
        if ( m < v ):
            visible += 1
            continue
print("Part 1:",visible)
scores = []
for x in range(1, len(grid)-1):
    for y in range(1, len(grid[0])-1):
        v = grid[x][y]
        xx = x-1
        # Check up
        m = 0
        score = []
        d = 1
        while ( xx >= 0 ):
            vv = grid[xx][y]
            if ( vv >= v or xx == 0):
                score.append(d)
                break
            d += 1
            xx -= 1
        xx = x+1
        # Check down
        m = 0
        d = 1
        while ( xx < len(grid) ):
            vv = grid[xx][y]
            if ( vv >= v  or xx == len(grid)-1):
                score.append(d)
                break
            xx += 1
            d += 1
        # Check left
        m = 0
        d = 1
        yy = y-1
        while ( yy >= 0 ):
            vv = grid[x][yy]
            if ( vv >= v or yy == 0):
                score.append(d)
                break
            yy -= 1
            d += 1
        # Check right
        m = 0
        yy = y+1
        d = 1
        while ( yy < len(grid[0]) ):
            vv = grid[x][yy]
            if ( vv >= v or yy == len(grid[0])-1):
                score.append(d)
                break
            yy += 1
            d += 1
        s = 1
        for sc in score:
            s *= sc
        scores.append(s)

print("Part 2:", max(scores))

