import matplotlib.pyplot as plt
import numpy as np

# change this file name to the spreadsheet
f = open("file.csv", "r")

# (optional) tag matches with a competition
comp = ""
# weights for overall score (tentative numbers)
weights = [0, 0, 0, 2, 4, 6, 0, 1, 2, 3, 10, 20, 1, 2, 3, 0, 0, 0, -0.25]
# dictionary for keeping track of the teams
teams = {}
if f.mode == 'r':
    contents = f.readlines()
    # read all of the labels
    labels = contents[0].replace('"','').split(",")
    # loop through scouting data
    for i in range(1, len(contents)):
        data = contents[i].split(',')
        # team number is first value
        team = int(data[0].replace('"',''))
        # match number is second value
        match = int(data[1].replace('"',''))
        matchtag = comp + " match " + str(match)
        # initialize uninitialized team dictionaries
        if not team in teams:
            teams[team] = {}
        # add match to dictionary
        teams[team][matchtag] = {}

        # initialize sum counters
        ballScore = 0
        climbScore = 0
        controlScore = 0
        totalBalls = 0
        autoBalls = 0
        teleopBalls = 0
        teleopBallsBottom = 0
        teleopBallsOuter = 0
        teleopBallsInner = 0
        teleopBallScore = 0
        autoBallScore = 0
        score = 0
        for j in range(3, len(data)):
            value = data[j].replace('"','')
            #rotational control
            if j == 10:
                if value == "y":
                    score+=10
                    controlScore+=10
                    teams[team][matchtag][labels[j]]=10
                else:
                    teams[team][matchtag][labels[j]]=0
                continue
            elif j>=3 and j<=5:
                balls = int(value)
                autoBalls+=balls
                score+=balls*weights[j]
                autoBallScore+=balls*weights[j]
                ballScore+=balls*weights[j]
                teams[team][matchtag][labels[j]]=int(value)
            elif j==7 or j==12:
                balls = int(value)
                teleopBalls+=balls
                teleopBallsBottom+=balls
                score+=balls*weights[j]
                teleopBallScore+=balls*weights[j]
                ballScore+=balls*weights[j]
                teams[team][matchtag][labels[j]]=int(value)
            elif j==8 or j==13:
                balls = int(value)
                teleopBalls+=balls
                teleopBallsOuter+=balls
                score+=balls*weights[j]
                teleopBallScore+=balls*weights[j]
                ballScore+=balls*weights[j]
                teams[team][matchtag][labels[j]]=int(value)
            elif j==9 or j==14:
                balls = int(value)
                teleopBalls+=balls
                teleopBallsInner+=balls
                score+=balls*weights[j]
                teleopBallScore+=balls*weights[j]
                ballScore+=balls*weights[j]
                teams[team][matchtag][labels[j]]=int(value)
            elif j == 11:
                if value == "y":
                    score += 20
                    controlScore+=20
                    teams[team][matchtag][labels[j]]=20
                else:
                    teams[team][matchtag][labels[j]]=0
                continue
            #scoring locations
            elif j == 15:
                teams[team][matchtag][labels[j]]=value
                continue
            #hang
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
            #defense and climb
            elif j == 17 or j==18:
                teams[team][matchtag][labels[j]]=int(value)
            else:
                teams[team][matchtag][labels[j]]=int(value)
                score+=int(value)*weights[j]
                ballScore+=int(value)*weights[j]
                totalBalls+=int(value)
        #populate some general statistics from the match
        teams[team][matchtag]["Overall Score"] = score
        teams[team][matchtag]["Total Ball Score"] = ballScore
        teams[team][matchtag]["Auto Ball Score"] = autoBallScore
        teams[team][matchtag]["Teleop Ball Score"] = teleopBallScore
        teams[team][matchtag]["Teleop Balls Bottom"] = teleopBallsBottom
        teams[team][matchtag]["Teleop Balls Outer"] = teleopBallsOuter
        teams[team][matchtag]["Teleop Balls Inner"] = teleopBallsInner
        teams[team][matchtag]["Climb Score"] = climbScore
        teams[team][matchtag]["Total Balls"] = totalBalls
        teams[team][matchtag]["Control Score"] = controlScore

#used to get the average value of a metric for a team
def getAverageBetweenMatches(teams, team, datapoint):
    total = 0
    amount = 0
    for match in teams[team]:
        total+= teams[team][match][datapoint]
        amount+=1
    return total/amount

metrics = ["Bottom Port Auto", "Outer Port Auto", "Inner Port Auto", "PC Pickup Auto", "Teleop Balls Bottom", "Teleop Balls Outer", "Teleop Balls Inner", "Rotation Control", "Position Control", "Overall Score", "Total Ball Score", "Climb Score", "Total Balls", "Control Score", "Auto Ball Score", "Teleop Ball Score"]
print("1 | data on a specific team")
print("2 | single metric across all teams")
print("3 | compare multiple teams")
graphType = input()
if graphType == "1":
    # get all data for a single team
    print("team?")
    team = int(input())
    labels = ["Bottom Port Auto","Outer Port Auto","Inner Port Auto","PC Pickup Auto","Bottom Port Tele","Outer Port Tele","Inner Port Tele","Rotation Control","Position Control","Bottom Port Endgame","Outer Port Endgame","Inner Port Endgame","Endgame Outcome","Defense Second", "Overall Score", "Ball Score", "Climb Score", "Total Balls"]
    # graph
    ind = np.arange(len(labels))
    values = []
    for label in labels:
        values.append(getAverageBetweenMatches(teams, team, label))
    # get indices for a sort by values
    sortedListIndices = np.flip(np.argsort(values))
    sortedlabels = []
    sortedvalues = []
    # make sorted labels and values
    for i in range(len(sortedListIndices)):
        sortedlabels.append(labels[sortedListIndices[i]])
        sortedvalues.append(values[sortedListIndices[i]])
    plt.bar(ind, sortedvalues)
    plt.xlabel('Category', fontsize=7)
    plt.ylabel('Value', fontsize=7)
    plt.xticks(ind, sortedlabels, fontsize=7, rotation=30)
    plt.title(team)
    plt.show()
elif graphType == "2":
    #get single metric for all teams
    labels = list(teams.keys())
    
    # print metric options
    print("0 | Bottom Port Auto")
    print("1 | Outer Port Auto")
    print("2 | Inner Port Auto")
    print("3 | PC Pickup Auto")
    print("4 | Bottom Port Tele")
    print("5 | Outer Port Tele")
    print("6 | Inner Port Tele")
    print("7 | Rotation Control")
    print("8 | Position Control")
    print("9 | Overall Score")
    print("10| Total Ball Score")
    print("11| Climb Score")
    print("12| Total Balls")
    print("13| Control Score")
    print("14| Auto Ball Score")
    print("15| Teleop Ball Score")
    print("enter the desired data point")

    #graph
    datapoint = metrics[int(input())]
    ind = np.arange(len(labels))
    values = []
    for team in labels:
        values.append(getAverageBetweenMatches(teams, team, datapoint))
    sortedindices = np.flip(np.argsort(values))
    sortedlabels=[]
    sortedvalues=[]
    for i in range(len(sortedindices)):
        sortedlabels.append(labels[sortedindices[i]])
        sortedvalues.append(values[sortedindices[i]])
    plt.bar(ind, sortedvalues)
    plt.xlabel('Team', fontsize=7)
    plt.ylabel('Value', fontsize=7)
    plt.xticks(ind, sortedlabels, fontsize=7, rotation=30)
    plt.title(datapoint)
    plt.show()
elif graphType == "3":
    selected = []
    team = ""
    print("Enter teams and then enter q when done")
    while True:
        team = input()
        if(team == "q"):
            break
        selected.append(int(team))
    print(selected)
    labels = ["Bottom Port Auto","Outer Port Auto","Inner Port Auto","PC Pickup Auto","Bottom Port Tele","Outer Port Tele","Inner Port Tele","Rotation Control","Position Control","Bottom Port Endgame","Outer Port Endgame","Inner Port Endgame","Endgame Outcome","Defense Second", "Overall Score", "Ball Score", "Climb Score", "Total Balls"]
    # graph
    ind = np.arange(len(labels))
    width = 0.75/len(selected)
    for i in range(len(selected)):
        values = []
        for label in labels:
            values.append(getAverageBetweenMatches(teams, selected[i], label))
        plt.bar(ind + (i-len(selected)/2.0 + 0.5)*width, values, width, label=selected[i])
    plt.xlabel('Category', fontsize=7)
    plt.ylabel('Value', fontsize=7)
    plt.xticks(ind, labels, fontsize=7, rotation=30)
    plt.legend()
    plt.show()
