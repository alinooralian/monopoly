import json

with open("leaderboard.json", "r", encoding="utf-8") as f:
    info = json.load(f)

print("Rate\tName\tWins\tMaximum Money")

row = []
for key in info.keys():
    row.append((info[key]["win_count"], info[key]["money"], info[key]["username"]))

leaderboard = sorted(row, reverse=True)
R = 1
for i in range(len(leaderboard)):
    print(f"{R}\t{leaderboard[i][2]}\t  {leaderboard[i][0]}\t    {leaderboard[i][1]}")
    R += 1