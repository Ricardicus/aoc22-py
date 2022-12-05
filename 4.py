from general import *

lines = readlinesFromFile("inputs/4.txt")

count = 0
count2 = 0
for line in lines:
    line = line.strip()
    pair = line.split(",")
    p1 = [ int(x) for x in pair[0].split("-") ]
    p2 = [ int(x) for x in pair[1].split("-") ]

    if ( p2[0] <= p1[0] and p2[1] >= p1[1] ):
        print(p2, "contains", p1)
        count += 1
    elif (p1[0] <= p2[0] and p1[1] >= p2[1]):
        print(p1, "contains" ,p2)
        count += 1
    
    if (p1[0] >= p2[0] and p1[0] <= p2[0] ):
        count2 += 1
    elif (p2[0] >= p1[0] and p2[0] <= p1[0] ):
        count2 += 1
    elif (p1[1] >= p2[0] and p1[1] <= p2[1] ):
        count2 += 1
    elif (p2[1] >= p1[0] and p2[1] <= p1[1] ):
        count2 += 1    

print("Part 1:",count)
print("Part 2:",count2)
