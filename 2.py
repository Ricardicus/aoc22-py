from general import *

lines = readlinesFromFile("inputs/2.txt")
rounds = []
for line in lines:
    op = line.split(" ")
    they = op[0]
    we = op[1].strip()
    op = [they, we]
    rounds.append(op)

op_wins = {
    "A" : "Z",
    "B" : "X",
    "C" : "Y"
}

we_win = {
    "Y" : "A",
    "X" : "C",
    "Z" : "B",
    "A" : 2,
    "B" : 3,
    "C" : 1
    }


we_lose = {
        "A" : 3,
        "B" : 1,
        "C" : 2
}

scorePlay = {
    "X":1, "Y":2, "Z" : 3
}

we_draw = { "X" : "A", "Y": "B", "Z" : "C", "A" : 1, "B": 2, "C":3 }

def countScore(plays):
    score = 0
    for play in plays:
        op = play[0]
        we = play[1]

        if we_win[we] == op:
            score += 6
        elif we_draw[we] == op:
            score += 3

        score += scorePlay[we]
    return score

print(countScore(rounds))

def countScore2(plays):
    score = 0
    for play in plays:
        op = play[0]
        we = play[1]
        
        if we == "X": 
            # loose 
            score += we_lose[op]
            print("lose" , play, (we_lose[op]))
        elif we == "Y": 
            # draw
            print("draw ", play, (3+we_draw[op]))
            score += 3 + we_draw[op]
        else:
            # win
            print("win ", play, (6+we_win[op]))
            score += 6 + we_win[op]

    return score

print(countScore2(rounds))
