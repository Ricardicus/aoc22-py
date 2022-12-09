from general import *

lines = readlinesFromFile("inputs/9.txt")

start = [0,0]
head_pos = [[0,0]]
tail_pos = [[0,0]]

for line in lines:
    f = line.strip().split(" ")[0]
    a = int(line.strip().split(" ")[1])
    new_pos = head_pos[-1].copy()
    if ( f == "R" ):
        q = 0
        while ( q < a ):
            new_pos[1] += 1
            head_pos.append(new_pos.copy()) 
            q += 1
    elif ( f == "U" ):
        q = 0
        while ( q < a ):
            new_pos[0] += 1
            head_pos.append(new_pos.copy()) 
            q += 1
    elif ( f == "L" ):
        q = 0
        while ( q < a ):
            new_pos[1] -= 1
            head_pos.append(new_pos.copy()) 
            q += 1
    elif ( f == "D" ):
        q = 0
        while ( q < a ):
            new_pos[0] -= 1
            head_pos.append(new_pos.copy()) 
            q += 1

def get_distance(a, b):
    d1 = a[0] - b[0]
    d2 = a[1] - b[1]
    return [d1, d2]

def get_new_tail(head, tail):
    tail = tail.copy()
    diff = get_distance(head, tail)
    if diff[0] == 0 and diff[1] == 0:
        return tail.copy()
    if abs(diff[0]) == 1 and abs(diff[1]) == 1:
        return tail.copy()
    if abs(diff[0]) == 2 and abs(diff[1]) == 1:
        return [tail[0]+int(diff[0]/2), tail[1]+diff[1]]
    if abs(diff[0]) == 1 and abs(diff[1]) == 2:
        return [tail[0]+diff[0], tail[1]+int(diff[1]/2)]
    if abs(diff[0]) == 2 and diff[1] == 0:
        return [tail[0]+int(diff[0]/2), tail[1]]
    if diff[0] == 0 and abs(diff[1]) == 2:
        return [tail[0], tail[1] + int(diff[1]/2)]
    if abs(diff[0]) == 2 and abs(diff[1]) == 2:
        return [tail[0] + int(diff[0]/2), tail[1] + int(diff[1]/2)]
    return tail.copy()

tail_pos = [start]

grid_len = max( [x[0] for x in head_pos])
grid_len_2 = max ( [ x[1] for x in head_pos] )

for pos in head_pos:
    t = tail_pos[-1]
    t2 = get_new_tail(pos, t)
    tail_pos.append(t2)

q = set()
for pos in tail_pos:
    p = str(pos[0]) + "," + str(pos[1])
    q.add(p)

print("Part 1:", len(q))
tails = [ start.copy() for x in range(9) ]
tail_last = [start]
ss = []
for pos in head_pos:
    for i in range(8, -1, -1):
        if ( i == 8 ):
            t2 = get_new_tail(pos, tails[i])
            tails[i] = t2
        else:
            tails[i] = get_new_tail(tails[i+1], tails[i])
    tail_last.append(tails[0].copy())
    s = str(tails[0][0]) + "," + str(tails[0][1])
    if ( s not in ss ) :
        ss.append(s)

q = set()
for pos in tail_last:
    p = str(pos[0]) + "," + str(pos[1])
    q.add(p)
print("Part 2:", len(q))


