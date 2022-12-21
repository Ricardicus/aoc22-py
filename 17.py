from general import *
import time
import sys

dataFile = "inputs/17.txt"

if len(sys.argv) > 1 and sys.argv[1] == "small":
    dataFile += ".small"
print(dataFile)
lines = readlinesFromFile(dataFile)
lines = [ line.strip() for line in lines ]

# directions
LEFT = -1
RIGHT = 1

# objects
AIR = 0
ROCK = 1

# Input
pushes = []
line = lines[0]
for c in line:
    if c == "<":
        pushes.append(LEFT)
    elif c == ">":
        pushes.append(RIGHT)
#print(pushes)

# Initialize grid
gridHeight = 100000
gridwidth = 7
grid = []
for i in range(gridHeight):
    grid.append([])
    for q in range(7):
        grid[i].append(AIR)

def displayGrid(upto):
    s = ""
    for i in range(upto):
        ii = gridHeight - upto + i 
        for q in range(7):
            if grid[ii][q] == AIR:
                s += "."
            elif grid[ii][q] == ROCK:
                s += "#"
        s += "\n"
    print(s)

rocks = [
[[ROCK, ROCK, ROCK,ROCK]],
[[AIR, ROCK, AIR],[ROCK, ROCK, ROCK],[AIR,ROCK,AIR]],
[[AIR, AIR, ROCK],[AIR,AIR,ROCK], [ROCK,ROCK,ROCK]],
[[ROCK],[ROCK],[ROCK],[ROCK]],
[[ROCK, ROCK],[ROCK,ROCK]]
]

class Rock:
    def __init__(self, rockType, startHeight):
        self._type = rockType
        self._y = startHeight
        self._model = rocks[rockType]
        self.bottom = 0
        self.stopped = False

        modelH = len(self._model)

        self.currentPos = [startHeight-modelH+1, 2]
        self.top = self.currentPos[0]

    def hasStopped(self):
        return self.stopped

    def getTop(self):
        return self.top

    def push(self, direction):
        tmp = self.currentPos[1]
        self.currentPos[1] += direction
        if self.currentPos[1] + len(self._model[0]) > 7:
            # Over correct
            self.currentPos[1] = tmp
        elif self.currentPos[1] < 0:
            # Over correct
            self.currentPos[1] = tmp
        # Did we hit anything?
        for i in range(len(self._model)):
            for q in range(len(self._model[0])):
                if self._model[i][q] == ROCK:
                    if grid[self.currentPos[0] + i][self.currentPos[1] + q] == ROCK:
                        # Yes, we did, not good
                        self.currentPos[1] = tmp
                        break

    def fall(self):
        # Check if it is going to crash
        # Find bottom pos
        bottom = len(self._model)-1
        bottomTot = self.currentPos[0] + bottom
        if ( bottomTot + 1 >= gridHeight ):
            self.stopped = True
            return
        for i in range(len(self._model)):
            for q in range(len(self._model[0])):
                if self._model[i][q] == ROCK:
                    if grid[self.currentPos[0]+i+1][self.currentPos[1]+q] == ROCK:
                        # Blocked below, stopping
                        self.stopped = True
                        return
        # OK
        self.currentPos[0] += 1

    def clear(self):
        for i in range(len(self._model)):
            for q in range(len(self._model[0])):
                if self._model[i][q] == ROCK:
                    grid[self.currentPos[0] + i][self.currentPos[1] + q] = AIR 
                    self.bottom = i

    def draw(self):
        for i in range(len(self._model)):
            for q in range(len(self._model[0])):
                if self._model[i][q] == ROCK:
                    if i == 0:
                        self.top = self.currentPos[0]
                    grid[self.currentPos[0] + i][self.currentPos[1] + q] = ROCK
                    self.bottom = i  

def partOne():
    keep_running = True
    startHeight = gridHeight - 4
    index = 0
    rockIndex = 0
    top = 0
    prevStartHeight = 0
    while keep_running:
        r = Rock(rockIndex % 5, startHeight)
        prevStartHeight = startHeight
        top = r.getTop()
        
        while not r.hasStopped():
            p = pushes[index % len(pushes)]
            r.draw()
            #displayGrid(40)
            #time.sleep(0.1)
            r.clear()
            r.push(p)
            r.draw()
            #displayGrid(40)
            #time.sleep(0.1)
            r.clear()
            r.fall()
            r.draw()
            #displayGrid(40)
            #time.sleep(0.1)
            if not r.hasStopped():
                r.clear()
            else:
                startHeight = r.getTop() - 4
                if prevStartHeight < startHeight:
                    startHeight = prevStartHeight

            top = r.getTop()
            index += 1


        #print(gridHeight - top)
        rockIndex += 1
        if rockIndex == 2022:
            break

    print(gridHeight-top)

def checkGrid():
    bottom = len(grid)
    limit = 200
    hurdles = [0,0,0,0,0,0,0]
    for q in range(len(grid[0])):    
        for i in range(limit):
            r = bottom - 1 - i
            if grid[r][q] == ROCK:
                hurdles[q] = i
    if any([ x == 0 for x in hurdles ]):
        return 0
    return min(hurdles)

def getGridKey():
    row = 1000
    s = ""
    for i in range(row):
        for q in range(len(grid[0])):    
            if ( grid[len(grid)-1-i][q] == ROCK ):
                s += "#"
            else:
                s += "."
        s += ":"
    return s

def initGrid():
    global grid
    grid = []
    for i in range(gridHeight):
        grid.append([])
        for q in range(7):
            grid[i].append(AIR)

def moveGrid(s):
    global grid
    i = 0
    while ( i < s ):
        grid.pop()
        grid.insert(0,[AIR for _ in range(7)])
        i+=1

def partTwo():
    nbrRocks = 5
    nbrGasCycles = len(pushes)
    
    initGrid()
    keep_running = True
    startHeight = gridHeight - 4
    shifted = 0
    index = 0
    rockIndex = 0
    top = 0
    prevStartHeight = 0
    cache = {}
    limit = 1000000000000
    towerHeight = 0
    keyFound = False
    while rockIndex < limit:

        r = Rock(rockIndex % 5, startHeight)
        prevStartHeight = startHeight
     
        towerHeight = gridHeight + shifted - startHeight - 4 
        key = getGridKey() + "," + str(rockIndex % 5) + "," + str(index%len(pushes))
        if key in cache and not keyFound:
            heightLastTime, idxLastTime = cache[key]
            idxDiff = rockIndex - idxLastTime 
            diff = towerHeight - heightLastTime 
            iteratations, offset = divmod(limit-rockIndex, idxDiff)
            rockIndex += iteratations * idxDiff
            shifted += diff*iteratations
            displayGrid(10)
            keyFound = True
            #index += 1
            #rockIndex += 1
            #continue
        else:
            cache[key] = [towerHeight, rockIndex]

        while not r.hasStopped():

            r.draw()
            #displayGrid(40)
            #time.sleep(0.1)
            #print(checkGrid())
            r.clear()
            p = pushes[index % len(pushes)]
            r.push(p)
            index += 1
            #r.draw()
            #displayGrid(40)
            #time.sleep(0.1)
            #print(checkGrid())
            #r.clear()
            r.fall()
            r.draw()
            #displayGrid(40)
            #time.sleep(0.1)
            #print(checkGrid())
            if not r.hasStopped():
                r.clear()
            startHeight = r.getTop() - 4
            if prevStartHeight < startHeight:
                startHeight = prevStartHeight

        towerHeight = gridHeight + shifted - startHeight - 4 

# This checking of the grid, removing the
# down side, messed up part 2, but looks 
# really nice as a feature for tetris!
#        s = checkGrid()
#        if s > 0:
#            moveGrid(s)
#            shifted += s
#            startHeight += s
            #print(startHeight)

        rockIndex += 1
        #displayGrid(10)
        #print(towerHeight)
        #time.sleep(0.1)
    print(towerHeight)
partOne()
partTwo()



