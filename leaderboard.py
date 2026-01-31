from rich.console import Console
from rich.table import Table
import json
from colorama import init, Fore, Back, Style

init()

with open("leaderboard.json", "r", encoding="utf-8") as f:
    info = json.load(f)

console = Console()


table = Table(title=Fore.GREEN + "Leaderboard" + Style.RESET_ALL, style="magenta")

table.add_column("Rate", justify="cneter", no_wrap=True)
table.add_column("Name", justify="center", no_wrap=True)
table.add_column("Wins", justify="center", no_wrap=True)
table.add_column("Maximum Money", justify="center", no_wrap=True)

row = []
for key in info.keys():
    row.append((info[key]["win_count"], info[key]["money"], info[key]["username"]))

leaderboard = sorted(row, reverse=True)

for R, i in enumerate(leaderboard, 1):
    if R == 1:
        table.add_row(R, i[2], i[0], i[1], style="bold yellow")
    elif R == 2:
        table.add_row(R, i[2], i[0], i[1], style="bold white")
    elif R == 3:
        table.add_row(R, i[2], i[0], i[1], style="bold orange")
    else:
        table.add_row(R, i[2], i[0], i[1])

console.print(table)