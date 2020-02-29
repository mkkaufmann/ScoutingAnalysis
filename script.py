import matplotlib.pyplot as plt
import statistics

f = open("file.csv", "r")

weights = [0, 0, 0, 2, 4, 6, 0, 1, 2, 3, 10, 20, 1, 2, 3, 0, 0, 0, -0.25]
teams = {}

if f.mode == 'r':
    contents = f.readlines()
    for i in range(1, len(contents)):
        data = contents[i].split(',')
        team = int(data[0].replace('"',''))
        score = 0;
        for j in range(3, len(data)):
            value = data[j].replace('"','')
            if j == 10:
                if value == "y":
                    score+=10
                continue
            elif j == 11:
                if value == "y":
                    score += 20
                continue
            elif j == 15:
                continue
            elif j == 16:
                if value == "L":
                    score += 30
                elif value == "H":
                    score += 25
                continue
            else:
                increase = int(value)*weights[j]
                score+=int(value)*weights[j]
        if team in teams:
            teams[team].append(score)
        else:
            teams[team] = [score]
x = list(teams.keys())
y = []
for team in x:
    y.append(statistics.mean(teams[team]))
plt.plot(x, y)
plt.xlabel('team')
plt.ylabel('avg score')
plt.title('scores')
plt.show()


