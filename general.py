def readlinesFromFile(file):
    f = open(file, "r")
    l = f.readlines()
    f.close()
    return l

def readlinesAsIntsFromFile(file):
    lines = readlinesFromFile(file)
    l = []
    for line in lines:
        l.append(int(line))
    return l


