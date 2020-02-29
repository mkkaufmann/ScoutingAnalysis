import matplotlib.pyplot as plt
import numpy as np

f = open("file.csv", "r")

comp = "stjoe"
weights = [0, 0, 0, 2, 4, 6, 0, 1, 2, 3, 10, 20, 1, 2, 3, 0, 0, 0, -0.25]
teams = {}
if f.mode == 'r':
    contents = f.readlines()
    labels = contents[0].replace('"','').split(",")
    for i in range(1, len(contents)):
        data = contents[i].split(',')
        team = int(data[0].replace('"',''))
        match = int(data[1].replace('"',''))
        matchtag = comp + " match " + str(match)
        if not team in teams:
            teams[team] = {}
        teams[team][matchtag] = {}
        ballScore = 0
        climbScore = 0
        controlScore = 0
        totalBalls = 0
        score = 0
        for j in range(3, len(data)):
            value = data[j].replace('"','')
            if j == 10:
                if value == "y":
                    score+=10
                    controlScore+=10
                    teams[team][matchtag][labels[j]]=10
                else:
                    teams[team][matchtag][labels[j]]=0
                continue
            elif j == 11:
                if value == "y":
                    score += 20
                    controlScore+=20
                    teams[team][matchtag][labels[j]]=20
                else:
                    teams[team][matchtag][labels[j]]=0
                continue
            elif j == 15:
                teams[team][matchtag][labels[j]]=value
                continue
            elif j == 16:
                if value == "L":
                    teams[team][matchtag][labels[j]]=40
                    score += 40
                    climbScore += 40
                elif value == "H":
                    teams[team][matchtag][labels[j]]=25
                    score += 25
                    climbScore += 25
                elif value == "P":
                    teams[team][matchtag][labels[j]]=5
                    score += 5
                    climbScore += 5
                else:
                    teams[team][matchtag][labels[j]]=0
                continue
            elif j == 17 or j==18:
                teams[team][matchtag][labels[j]]=int(value)
            else:
                teams[team][matchtag][labels[j]]=int(value)
                increase = int(value)*weights[j]
                score+=int(value)*weights[j]
                ballScore+=int(value)*weights[j]
                totalBalls+=1
        teams[team][matchtag]["Overall Score"] = score
        teams[team][matchtag]["Ball Score"] = ballScore
        teams[team][matchtag]["Climb Score"] = climbScore
        teams[team][matchtag]["Total Balls"] = totalBalls
        teams[team][matchtag]["Control Score"] = controlScore

def getAverageBetweenMatches(teams, team, datapoint):
    total = 0
    amount = 0
    for match in teams[team]:
        total+= teams[team][match][datapoint]
        amount+=1
    return total/amount

metrics = ["Bottom Port Auto", "Outer Port Auto", "Inner Port Auto", "PC Pickup Auto", "Bottom Port Tele", "Outer Port Tele", "Inner Port Tele", "Rotation Control", "Position Control", "Bottom Port Endgame", "Outer Port Endgame", "Inner Port Endgame", "Overall Score", "Ball Score", "Climb Score", "Total Balls", "Control Score"]
print("data on a specific team? y/n")
specific = input()
if specific == "y":
    print("team?")
    team = int(input())
    labels = ["Bottom Port Auto","Outer Port Auto","Inner Port Auto","PC Pickup Auto","Bottom Port Tele","Outer Port Tele","Inner Port Tele","Rotation Control","Position Control","Bottom Port Endgame","Outer Port Endgame","Inner Port Endgame","Endgame Outcome","Defense Second", "Overall Score", "Ball Score", "Climb Score", "Total Balls"]
    ind = np.arange(len(labels))
    values = []
    for label in labels:
        values.append(getAverageBetweenMatches(teams, team, label))
    plt.bar(ind, values)
    plt.xlabel('Category', fontsize=7)
    plt.ylabel('Value', fontsize=7)
    plt.xticks(ind, labels, fontsize=7, rotation=30)
    plt.title(team)
    plt.show()
else:
    labels = list(teams.keys())

    print("0 | Bottom Port Auto")
    print("1 | Outer Port Auto")
    print("2 | Inner Port Auto")
    print("3 | PC Pickup Auto")
    print("4 | Bottom Port Tele")
    print("5 | Outer Port Tele")
    print("6 | Inner Port Tele")
    print("7 | Rotation Control")
    print("8 | Position Control")
    print("9 | Bottom Port Endgame")
    print("10| Outer Port Endgame")
    print("11| Inner Port Endgame")
    print("12| Overall Score")
    print("13| Ball Score")
    print("14| Climb Score")
    print("15| Total Balls")
    print("16| Control Score")
    print("enter the desired data point")
    datapoint = metrics[int(input())]
    ind = np.arange(len(labels))
    values = []
    for team in labels:
        values.append(getAverageBetweenMatches(teams, team, datapoint))
    plt.bar(ind, values)
    plt.xlabel('Team', fontsize=7)
    plt.ylabel('Value', fontsize=7)
    plt.xticks(ind, labels, fontsize=7, rotation=30)
    plt.title(datapoint)
    plt.show()


