from general import *
import re

lines = readlinesFromFile("inputs/7.txt")
fs = {}

def get_contents(index, base):
    i = index
    content = {}
    while ( i < len(lines) and lines[i][0] != "$" ):
        line = lines[i].strip()
        name = line.split(" ")[1]
        if ( line[0].isnumeric() ) :
            fs[base+"/"+name+"/"] = int(line.split(" ")[0])
        elif ( line.startswith("dir") ):
            fs[base+"/"+name+"/"] = "dir"
        i += 1
    fs[base] = content

visited = {}

def get_file_size(loc):
    if fs[loc] == "dir":
        c = 0
        for k in fs:
            if ( k.startswith(loc) and k != loc and k not in visited and fs[k] != None ):
                visited[k] = get_file_size(k)
                c += visited[k]
        return c
    else:
        if loc+"/" in visited:
            return visited[loc+"/"]
        else:
            visited[loc] = fs[loc]
        return fs[loc]

i = 0
root = ""
current = "" 
loc = []
while ( i < len(lines) ):
    line = lines[i].strip()
    s = line.split(" ")
    if ( s[1] == "cd" ):
        if (s[2] == ".."):
            loc.pop()
        else:
            current = s[2]
            if current == "/":
                current = ""
            loc.append(current)
            print("current",current)
    if s[1] == "ls":
        base = "/".join(loc)
        print("ls",base,loc)
        fs[base] = get_contents(i+1, base)
    i += 1
    print(loc)
fs["/"] = "dir"

print(fs)

print(get_file_size("/"))
print(visited)
print(fs)

countMax = 100000
count = 0
for k in visited:
    if visited[k] < countMax and fs[k] == "dir":
        count += visited[k]

print("Part 1:",count)
