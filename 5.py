from general import *

lines = readlinesFromFile("inputs/5.txt")
print(lines)
i = 0
while ( i < len(lines) ):
    print(lines[i])
    if len(lines[i]) < 2:
        break
    i += 1
instructions = []
i+=1
while ( i < len(lines) ):
    print(lines[i])
    q = lines[i].split(" ")
    instructions.append([int(q[1]), int(q[3]), int(q[5])])
    i += 1
print(instructions)

stacks = [[],
        ["B", "P", "N","Q", "H", "D", "R", "T"],
        ["W", "G", "B", "J", "T", "V"],
        ["N", "R", "H", "D", "S", "V", "M", "Q"],
        ["P", "Z", "N", "M", "C"],
        ["D", "Z", "B"],
        ["V", "C", "W", "Z"],
        ["G", "Z", "N", "C", "V", "Q", "L", "S"],
        ["L", "G", "J", "M", "D", "N", "V"],
        ["T", "P", "M", "F", "Z", "C", "G"]
    ]
for instruction in instructions:
    n = instruction[0]
    f = instruction[1]
    t = instruction[2]

    q = 0
    while ( q < n ):
        a = stacks[f].pop()
        stacks[t].append(a)
        q += 1

s = ""
i = 1
while ( i < len(stacks) ):
    s += stacks[i][-1]
    i += 1

print("Part 1:",s)
stacks = [[],
        ["B", "P", "N","Q", "H", "D", "R", "T"],
        ["W", "G", "B", "J", "T", "V"],
        ["N", "R", "H", "D", "S", "V", "M", "Q"],
        ["P", "Z", "N", "M", "C"],
        ["D", "Z", "B"],
        ["V", "C", "W", "Z"],
        ["G", "Z", "N", "C", "V", "Q", "L", "S"],
        ["L", "G", "J", "M", "D", "N", "V"],
        ["T", "P", "M", "F", "Z", "C", "G"]
    ]
for instruction in instructions:
    n = instruction[0]
    f = instruction[1]
    t = instruction[2]

    q = 0
    l = []
    while ( q < n ):
        a = stacks[f].pop()
        l.append(a)
        q += 1

    l = l[::-1]
    q = 0
    while ( q < len(l) ):
        stacks[t].append(l[q])
        q += 1

s = ""
i = 1
while ( i < len(stacks) ):
    s += stacks[i][-1]
    i += 1

print("Part 2:", s)
