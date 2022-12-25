from general import *
import sys

d = "inputs/25.txt"
partTwo = False
if len(sys.argv) > 1 and sys.argv[1] == "small":
    d += ".small"
if len(sys.argv) > 1 and sys.argv[1] == "2":
    partTwo = True

lines = readlinesFromFile(d)
lines = [ line[:-1] if line.endswith("\n") else line for line in lines ]

class SNAFUNumber:
    def __init__(self, value):
        if isinstance(value, str):
            v = 0
            q = 0
            for c in value[::-1]:
                if c.isnumeric():
                    v += int(c) * (5 ** q)
                elif c == "-":
                    v += -1 * (5 ** q)
                elif c == "=":
                    v += -2 * (5 ** q)
                q += 1
            self.snafu = value
            self.value = v
        elif isinstance(value, int):
            q = value
            fives = [0] * 30
            search = 0
            #print("Value:", value)
            snafu_digits = []

            while q > 0:
                r = q % 5
                carry = 0
                if r == 3:
                    snafu_digits.append("=")
                    carry = 1
                elif r == 4:
                    snafu_digits.append("-")
                    carry = 1 
                else:
                    snafu_digits.append(str(r))

                q = int(q/5) + carry
                search += 1
           
            snafu = "".join(snafu_digits[::-1])
            #print(snafu)
            #q = 0
            #for i, v in enumerate(snafu[::-1]):
            #    vv = 0
            #    if v == "=":
            #        vv = -2
            #    elif v == "-":
            #        vv = -1
            #    else:
            #        vv = int(v)
            #    q += (5 ** i) * vv
            #print("Back from snafu:", q)
            self.snafu = snafu
            self.value = value

        else:
            raise Exception("No!")

    def getSnafu(self):
        return self.snafu
    
    def getDecimal(self):
        return self.value

s = 0
for line in lines:
    snafu = SNAFUNumber(line)
    s += snafu.getDecimal()

print("Sum:", SNAFUNumber(s).getSnafu())

