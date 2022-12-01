# For now, just testing

from general import *

lines = readlinesFromFile("inputs/1.txt")
max_ = 0
count = 0

counts = [0]
count_i = 0

for line in lines:
    if len(line) == 1:
        counts.append(0)
        count = 0
        count_i += 1
    else:
        counts[count_i] += int(line)

print(counts)
counts.sort(reverse=True)
print(counts[0]+counts[1]+counts[2])
