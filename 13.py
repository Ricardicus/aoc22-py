from general import *
import ast
from functools import cmp_to_key

lines = readlinesFromFile("inputs/13.txt")
lines = [ line.strip() for line in lines ]

index = 1
q = 0
pairs = []
while q < len(lines):
    pairs.append([ast.literal_eval(lines[q]), ast.literal_eval(lines[q+1])])
    index += 1
    q += 3

def checkOrder(p1, p2):
    i = 0
    while i < len(p1):
        if i >= len(p2):
            return False
        if isinstance(p1[i], int) and isinstance(p2[i], int):
            if p1[i] > p2[i]:
                return False
            if p1[i] < p2[i]:
                return True
            i+=1
            continue
        a = p1[i]
        b = p2[i]
        if isinstance(p1[i], int) and isinstance(p2[i], list):
            a = [p1[i]]
        if isinstance(p1[i], list) and isinstance(p2[i], int):
            b = [p2[i]]
        if ( isinstance(a, list) and isinstance(b, list)):
            if len(a) == 0 and len(b) == 0:
                i += 1
                continue
            r = checkOrder(a, b) 
            if r is not None:
                return r
        i += 1
    if len(p1) < len(p2):
        return True
    if len(p2) > len(p1):
        return False
    return None

i = 0
s = 0
while ( i < len(pairs) ):
    b = checkOrder(*pairs[i])
    if b:
        s += (i+1)
    i += 1
    #import sys
    #sys.exit(0)

print(s)

class Comparer:
    def __init__(self, e):
        self.e = e
    def __lt__(self,other):
        r = checkOrder(self.e, other.e)
        return r
    def __gt__(self,other):
        return not checkOrder(self.e,other.e)
    def __repr__(self):
        return str(self.e)

lines = readlinesFromFile("inputs/13.txt")
lines = [ line.strip() for line in lines ]

pairs = []
pairs.append(Comparer([[2]]))
pairs.append(Comparer([[6]]))
q = 0
while q < len(lines):
    if ( lines[q] == "" ):
        q += 1
        continue
    pairs.append(Comparer(ast.literal_eval(lines[q])))
    q += 1
pairs.sort()
s = 1
q = 0
while q < len(pairs):
    p = str(pairs[q])
    if p == "[[2]]" or p == "[[6]]":
        s *= (q+1)
    q += 1
print(s)
