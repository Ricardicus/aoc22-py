
from general import *
import copy
import random
import threading
import sys

lines = readlinesFromFile("inputs/16.txt")
lines = [ line.strip() for line in lines ]

tunnels = {}
flow = 0

STAY = 0
MOVE = 1

cirlceMax = 4 # Arbitrary

for line in lines:
    print(line)
    p = line.split(" ")
    name = p[1]
    rate = int(p[4].split("=")[1][:-1])
    try:
        paths = line.split(" valves ")[1].split(", ")
    except IndexError:
        paths = [line.split(" valve ")[1]]
    paths.sort()
    tunnels[name] = { "name":name, "rate" : rate, "paths": paths, "open": False}

bestOptions = {}

nonzero_valves = [ name for name in tunnels.keys() if tunnels[name]["rate"] > 0 ]
#print([x["rate"] for x in nonzero_valves])
#sys.exit(0)

def distance(valves, a, b):
    if a == b:
        return 0
    seen = set()
    dist = 0
    search = []
    steps = 0
    for p in valves[a]["paths"]:
        search.append((p,1))
        seen.add(p)
    while len(search) > 0:
        valve, steps = search.pop(0)
        print(steps, a, b, valve)
        if valve == b:
            return steps
        for p in valves[valve]["paths"]:
            if p not in seen:
                seen.add(p)
                search.append((p, steps+1))
    print("None",a,b)
    return None

def wayOK(way):
    occurences = {}
    opened = 0

    for w in way:
        name = w[0]
        openstatus = w[1]
        if openstatus:
            opened += 1
        if name not in occurences:
            occurences[name] = { "count": 1, "opened": opened }
        else:
            if opened == occurences[name]["opened"]:
                return False
            occurences[name]["count"] += 1

    v = []
    for w in way:
        v.append(occurences[w[0]]["count"])
    v.sort(reverse=True)
    if v[0] < cirlceMax:
        return True
    return False

maxFlow = -1

def solve(name, valves, pressure, steps, ways):
    global maxFlow
    distances = {}
    for v in valves.keys():
        distances[v] = {}
        for t in nonzero_valves:
            distances[v][t] = distance(valves, v, t)
        print(v)

    states = [ {"minute": 1, "valve": "AA", "opened": [], "rate": 0, "total": 0 } ]
    maxFlow = 0

    while len(states) > 0:
        state = states.pop()
        maxFlow = max(maxFlow, state["total"]+(30-state["minute"]+1)*state["rate"])
        print(maxFlow)
        valve = valves[state["valve"]]
        if state["minute"] == 30:
            continue
        if state["valve"] not in state["opened"] and valve["rate"] > 0:
            states.append({"minute": state["minute"] + 1, "valve": state["valve"], "opened": state["opened"] + [state["valve"]],
                           "rate": state["rate"] + valve["rate"], "total" : state["total"] + state["rate"]})
            continue
        for d in nonzero_valves:
            if d in state["opened"]:
                continue
            dist = distances[state["valve"]][d]
            if (state["minute"] + dist) > 30:
                continue
            states.append({"minute": state["minute"] + dist, "valve": d, "opened": state["opened"], 
                           "rate": state["rate"], "total" : state["total"] + state["rate"]*dist})

def solvePart2(name, valves, pressure, steps, ways):
    global maxFlow
    distances = {}
    for v in valves.keys():
        distances[v] = {}
        for t in nonzero_valves:
            distances[v][t] = distance(valves, v, t)
        print(v)

    states = [ {"minute": 1, "valve": "AA", "opened": [], "rate": 0, "total": 0 } ]
    maxFlow = 0
    best_states = {}
    all_states = {}
    while len(states) > 0:
        state = states.pop()
        #print(maxFlow)
        valve = valves[state["valve"]]
        if state["minute"] == 26:
            continue
        if state["valve"] not in state["opened"] and valve["rate"] > 0:
            newState = {"minute": state["minute"] + 1, "valve": state["valve"], "opened": state["opened"] + [state["valve"]],
                           "rate": state["rate"] + valve["rate"], "total" : state["total"] + state["rate"] }
            states.append(newState)
            opened = newState["opened"]
            if len(opened) > 0:
                opened.sort()
                opened = str(opened)
                if opened not in best_states:
                    best_states[opened] = 0
                if best_states[opened] < newState["total"] + (26-newState["minute"]+1)*newState["rate"]:
                    best_states[opened] = newState["total"] + (26-newState["minute"]+1)*newState["rate"]
                    all_states[opened] = newState
            continue
        for d in nonzero_valves:
            if d in state["opened"]:
                continue
            dist = distances[state["valve"]][d]
            if (state["minute"] + dist) > 29:
                continue
            states.append({"minute": state["minute"] + dist, "valve": d, "opened": state["opened"], 
                           "rate": state["rate"], "total" : state["total"] + state["rate"]*dist})
    for person in all_states:
        person = all_states[person]
        for elephant in all_states:
            elephant = all_states[elephant]
            good_state = True
            for v in person["opened"]:
                if v in elephant["opened"]:
                    good_state = False
                    break
            if good_state:
                maxFlow = max(maxFlow, person["total"] + (26-person["minute"]+1)*person["rate"] + elephant["total"] + (26-elephant["minute"]+1)*elephant["rate"])

print("going in")
#solve("AA", tunnels, 0, 0, [])
#print(maxFlow)
solvePart2("AA", tunnels, 0, 0, [])
print(maxFlow)
print("Max flow:", maxFlow)
