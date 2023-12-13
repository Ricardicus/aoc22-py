import sys
lines = []
with open("inputs/12.txt", "r") as f:
    lines = f.readlines()

cache = {}
def arrangements(index, g_index, acc, groups, records, path):
    ret = 0
    key = "" + str(index) + "," + str(g_index) + "," + str(acc) + "," + str(groups) + "," + records
    if key in cache:
        return cache[key]
    if ( index == len(records) ):
        if ( g_index == len(groups) - 1 ):
            if ( acc > 0 and groups[g_index] == acc):
                return 1
            elif ( acc == 0 and records[index-1] == "#"):
                return 1
        elif ( g_index == len(groups) and path[-1] == "." and acc == 0 ):
            return 1
        else:
            return 0
    else:
        char = records[index]
        if (char == "."):
            if ( acc > 0 and g_index < len(groups) ):
                if ( groups[g_index] == acc ):
                    return arrangements(index+1, g_index+1, 0, groups, records, path+char)
            elif ( acc == 0 ):
                return arrangements(index+1, g_index, 0, groups, records, path + char)
        elif (char == "#"):
            return arrangements(index+1, g_index, acc+1, groups, records, path + char)
        elif (char == "?"):
            # if it was a dot
            if (acc >0 and g_index < len(groups)):
                if ( groups[g_index] == acc):
                    ret += arrangements(index+1, g_index+1,0, groups, records, path + ".")
            elif (acc == 0):
                ret += arrangements(index+1,g_index, 0, groups, records, path + ".")
            # if it was a '#'
            ret += arrangements(index +1, g_index, acc +1, groups, records, path + "#")
    cache[key] = ret
    return ret

def getNbrArrangements(line):
    groups = [ int(x) for x in line.split(" ")[1].split(",")]
    records = line.split(" ")[0]
    arr = arrangements(0, 0, 0, groups, records, "")
    return arr

sumPartOne = 0
for line in lines:
    sumPartOne += getNbrArrangements(line)

print("Part 1: ", sumPartOne)

sumPartTwo = 0
idx = 0
for line in lines:
    rules = line.split(" ")[0]
    groups = line.split(" ")[1]

    rules = "?".join([rules] * 5)
    groups = ",".join([groups] * 5)

    folded_line = rules + " " + groups
    idx += 1
    print(idx)
    a = getNbrArrangements(folded_line)
    sumPartTwo += a

print("Part 2: ", sumPartTwo)

