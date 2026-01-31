from rich.console import Console
from rich.table import Table
import json
from colorama import init, Fore, Back, Style

init()

console = Console()

table = Table(title=Fore.GREEN + "Scoreboard" + Style.RESET_ALL, style="magenta")

table.add_column("ID", justify="cneter", no_wrap=True)
table.add_column("Name", justify="center", no_wrap=True)
table.add_column("Position", justify="center", no_wrap=True)
table.add_column("Cash", justify="center", no_wrap=True)
table.add_column("Jail", justify="center", no_wrap=True)
table.add_column("Get out of jail card", justify="center", no_wrap=True)
table.add_column("Dice Counter", justify="center", no_wrap=True)
table.add_column("Property", justify="center", no_wrap=True)

colors = ["red", "blue", "green", "yellow"]
cnt = 0
for id in players.keys():
    table.add_row(id, players[id]["username"], players[id]["position"], players[id]["cash"], players[id]["jail"], players[id]["get_out_of_jail_card"], palyers[id]["dice_counter"], players[id]["property"], style=colors[cnt])
    cnt += 1

console.print(table)