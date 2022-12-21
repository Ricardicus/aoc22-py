from general import *
from enum import Enum
from collections import deque
from copy import deepcopy
import sys
import random

lines = readlinesFromFile("inputs/19.txt.2")
lines = [ line.strip() for line in lines ]

class Resources:
    def __init__(self):
        self.ore = 0
        self.clay = 0
        self.obs = 0
        self.geode = 0

    def increaseOre(self, v=1):
        self.ore += v
    def increaseClay(self, v=1):
        self.clay += v
    def increaseObsidian(self, v=1):
        self.obs += v
    def increaseGeode(self, v=1):
        self.geode += v

    def decreaseOre(self, v=1):
        self.ore -= v
    def decreaseClay(self, v=1):
        self.clay -= v
    def decreaseObsidian(self, v=1):
        self.obs -= v
    def decreaseGeode(self, v=1):
        self.geode -= v

    def getOre(self):
        return self.ore
    def getClay(self):
        return self.clay
    def getObsidian(self):
        return self.obs
    def getGeode(self):
        return self.geode

class Blueprint():
    def __init__(self, ore, clay, obs, geode):
        self.oreCost = ore
        self.clayCost = clay
        self.obsidianCost = obs
        self.geodeCost = geode

    def getCosts(self):
        return [self.oreCost, self.clayCost, self.obsidianCost, self.geodeCost]

    def affordsOreRobot(self, m: Resources):
        return m.getOre() >= self.oreCost
    def affordsClayRobot(self, m: Resources):
        return m.getOre() >= self.clayCost
    def affordsObsidianRobot(self, m: Resources):
        return m.getOre() >= self.obsidianCost[0] and m.getClay() >= self.obsidianCost[1]
    def affordsGeodeRobot(self, m: Resources):
        return m.getOre() >= self.geodeCost[0] and m.getObsidian() >= self.geodeCost[1]

    def highestOreCost(self):
        return max([self.oreCost, self.clayCost, self.obsidianCost[0], self.geodeCost[0]])
    def highestClayCost(self):
        return self.obsidianCost[1]
    def highestObsidianCost(self):
        return self.geodeCost[1]

    def buyOreRobot(self, m: Resources):
        if self.affordsOreRobot(m):
            m.decreaseOre(self.oreCost)
    def buyClayRobot(self, m: Resources):
        if self.affordsClayRobot(m):
            m.decreaseOre(self.clayCost)
    def buyObsidianRobot(self, m: Resources):
        if self.affordsObsidianRobot(m):
            m.decreaseOre(self.obsidianCost[0])
            m.decreaseClay(self.obsidianCost[1])
    def buyGeodeRobot(self, m: Resources):
        if self.affordsGeodeRobot(m):
            m.decreaseOre(self.geodeCost[0])
            m.decreaseObsidian(self.geodeCost[1])

bluePrints = []
for line in lines:
    s = line.split(" ")
    oreRobotCost = int(s[6])
    clayRobotCost = int(s[12])
    obsidianRobotCost = [int(s[18]),int(s[21])]
    geodeRobotCost = [int(s[27]), int(s[30])]
    b = Blueprint(oreRobotCost, clayRobotCost, obsidianRobotCost, geodeRobotCost)
    bluePrints.append(b)

WAIT = 0
BUY_ORE_ROBOT = 1
BUY_CLAY_ROBOT = 2
BUY_OBSIDIAN_ROBOT = 3
BUY_GEODE_ROBOT = 4
nbr_actions = 5

class State:
    def __init__(self, blueprint):
        self.resources = Resources()
        self.robots = [1,0,0,0]
        self.minute = 0
        self.actions = []
        self.blueprint = blueprint
    def update(self):
        newOres = self.robots[0]
        newClays = self.robots[1]
        newObsidians = self.robots[2]
        newGeodes = self.robots[3]
        self.resources.increaseOre(newOres)
        self.resources.increaseClay(newClays)
        self.resources.increaseObsidian(newObsidians)
        self.resources.increaseGeode(newGeodes)
        self.minute += 1

    def getResources(self):
        return self.resources

    def getMinute(self):
        return self.minute

    def getActionsLen(self):
        return len(self.actions)

    def canBuySomething(self):
        return self.canPerformAction(BUY_ORE_ROBOT) or self.canPerformAction(BUY_CLAY_ROBOT) or self.canPerformAction(BUY_OBSIDIAN_ROBOT) or self.canPerformAction(BUY_GEODE_ROBOT)

    def canPerformAction(self, action):
        if action == WAIT:
            return True 
        elif action == BUY_ORE_ROBOT:
            if not self.blueprint.affordsOreRobot(self.resources):
                return False
            if self.robots[0] >= self.blueprint.highestOreCost():
                return False
        elif action == BUY_CLAY_ROBOT:
            if not self.blueprint.affordsClayRobot(self.resources):
                return False
            if self.robots[1] >= self.blueprint.highestClayCost():
                return False
        elif action == BUY_OBSIDIAN_ROBOT:
            if not self.blueprint.affordsObsidianRobot(self.resources):
                return False
            if self.robots[2] >= self.blueprint.highestObsidianCost():
                return False
        elif action == BUY_GEODE_ROBOT:
            if not self.blueprint.affordsGeodeRobot(self.resources):
                return False
        return True

    def performAction(self, action):
        if action == WAIT:
            pass 
        elif action == BUY_ORE_ROBOT:
            if self.blueprint.affordsOreRobot(self.resources):
                self.blueprint.buyOreRobot(self.resources)
                self.robots[0] += 1
            else:
                return False
        elif action == BUY_CLAY_ROBOT:
            if self.blueprint.affordsClayRobot(self.resources):
                self.blueprint.buyClayRobot(self.resources)
                self.robots[1] += 1
            else:
                return False
        elif action == BUY_OBSIDIAN_ROBOT:
            if self.blueprint.affordsObsidianRobot(self.resources):
                self.blueprint.buyObsidianRobot(self.resources)
                self.robots[2] += 1
            else:
                return False
        elif action == BUY_GEODE_ROBOT:
            if self.blueprint.affordsGeodeRobot(self.resources):
                self.blueprint.buyGeodeRobot(self.resources)
                self.robots[3] += 1
            else:
                return False
        self.actions.append(str(action))
        return True

    def getYield(self):
        return self.resources.getGeode()

    def timesUp(self):
        return self.minute >= 32

    def getKey(self):
        return ",".join(self.actions)

    def getRobots(self):
        return self.robots

def evaluateBlueprint(blueprint):
    actions_seen = set()
    robots_seen = set()
    q = deque()
    state = State(blueprint)
    q.append(s)
    maxYield = 0
    c = blueprint.getCosts()
    loop = 0
    p = 0
    while p < 1000000:
        loop += 1
        #state = q.popleft()
        if state.timesUp():
            if state.getYield() > maxYield:
                maxYield = state.getYield()
                #print(maxYield)
            state = State(blueprint)
        else:
            #s = deepcopy(state)
            #k = s.getKey()
            #newKey = k + ","
            if state.canPerformAction(BUY_GEODE_ROBOT):
                #newKey += str(BUY_GEODE_ROBOT)
                #actions_seen.add(newKey)
                state.update()
                state.performAction(BUY_GEODE_ROBOT)
                #q.append(s)
            elif state.canPerformAction(BUY_OBSIDIAN_ROBOT):
                #newKey += str(BUY_OBSIDIAN_ROBOT)
                #actions_seen.add(newKey)
                state.update()
                state.performAction(BUY_OBSIDIAN_ROBOT)
                #q.append(s)
            elif state.canPerformAction(BUY_CLAY_ROBOT) and random.random() > 0.5:
                #newKey += str(BUY_CLAY_ROBOT)
                #actions_seen.add(newKey)
                state.update()
                state.performAction(BUY_CLAY_ROBOT)
                #q.append(s)
            elif state.canPerformAction(BUY_ORE_ROBOT) and random.random() > 0.5:
                #newKey += str(BUY_ORE_ROBOT)
                #actions_seen.add(newKey)
                state.update()
                state.performAction(BUY_ORE_ROBOT)
                #q.append(s)
            else:
                #newKey += str(WAIT)
                #actions_seen.add(newKey)
                state.update()
                state.performAction(WAIT)
                #q.append(s)
            """
            for i in range(0, nbr_actions):
                s = deepcopy(state)
                k = s.getKey()
                newKey = k + "," + str(i)
                if s.canPerformAction(BUY_GEODE_ROBOT) and i != BUY_GEODE_ROBOT:
                    continue
                elif s.canPerformAction(BUY_OBSIDIAN_ROBOT) and i != BUY_OBSIDIAN_ROBOT:
                    continue
                #elif s.canPerformAction(BUY_CLAY_ROBOT) and i != BUY_CLAY_ROBOT:
                #    if random.random() > 0.7:
                #        continue
                #r = s.getResources()
                #if r.getOre() > blueprint.highestOreCost() + 1 and i == WAIT:
                #    continue

                if newKey not in actions_seen and state.canPerformAction(i):
                    if loop % 10000 == 0:
                        print(newKey, maxYield, s.getActionsLen())
                    if s.getYield() > maxYield:
                        maxYield = s.getYield()
                    actions_seen.add(newKey)
                    s.update()
                    s.performAction(i)
                    q.append(s)
            """
        if p % 10000 == 0:
                print(maxYield, p, "(", 1000000 , ")")
        p += 1
    return maxYield

qualitySum = 1
for idx, blueprint in enumerate(bluePrints,1):
    my = evaluateBlueprint(blueprint)
    print("",idx, ":", my)
    qualitySum *= my
print("Part 2:",qualitySum)
