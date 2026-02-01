import tkinter as tk
from tkinter import messagebox
import random
import json
import uuid

with open("current_player.json", "r", encoding="utf-8") as f:
    current_player_data = json.load(f)

starter_id = current_player_data["current_player"]
starter_name = current_player_data["username"]

players = {}

players[starter_id] = {
    "username": starter_name,
    "cash": 1500,
    "position": 0,
    "property": {},
    "jail": False,
    "dice_counter": 3,
    "get_out_of_jail_card": False
}

for i in range(3):
    pid = str(uuid.uuid4())
    players[pid] = {
        "username": f"Bot {i+1}",
        "cash": 1500,
        "position": 0,
        "property": {},
        "jail": False,
        "dice_counter": 3,
        "get_out_of_jail_card": False
    }

players["bank"] = {"cash": float("inf")}

player_list = [p for p in players if p != "bank"]
current_player_index = 0

tiles = {
    2: "community",
    7: "chance",
    10: "jail",
    30: "gotojail"
}

def roll_dice():
    return random.randint(1,6), random.randint(1,6)

def pay(creditor, debtor, amount):
    players[debtor]["cash"] -= amount
    players[creditor]["cash"] += amount

def goto_jail(player):
    players[player]["position"] = 10
    players[player]["jail"] = True
    messagebox.showinfo("🚓 Jail", "Straight to jail 😭")

def give_jail_card(player):
    players[player]["get_out_of_jail_card"] = True

def advance_to(player, pos):
    if players[player]["position"] > pos:
        players[player]["cash"] += 200
    players[player]["position"] = pos

chance_cards = [
    ("✨ Advance to GO", lambda p: advance_to(p, 0)),
    ("🚓 Go to Jail", lambda p: goto_jail(p)),
    ("💵 Collect $50", lambda p: pay("bank", p, 50))
]

community_cards = [
    ("🗝 Get Out of Jail Free", lambda p: give_jail_card(p)),
    ("💰 Collect $100", lambda p: pay("bank", p, 100))
]

def next_turn():
    global current_player_index
    current_player_index = (current_player_index + 1) % len(player_list)
    update_gui()

def update_gui():
    p = player_list[current_player_index]
    current_label.config(text=f"💖 Turn: {players[p]['username']}")
    info_box.delete("1.0", tk.END)

    for pid in player_list:
        pl = players[pid]
        info_box.insert(
            tk.END,
            f"👤 {pl['username']} | 💰 {pl['cash']} | 📍 {pl['position']} | 🚓 {pl['jail']}\n"
        )

def roll_action():
    player = player_list[current_player_index]

    if players[player]["jail"]:
        if players[player]["get_out_of_jail_card"]:
            players[player]["jail"] = False
            players[player]["get_out_of_jail_card"] = False
        else:
            messagebox.showinfo("😭 Jail", "Turn skipped")
            next_turn()
            return

    d1, d2 = roll_dice()
    players[player]["position"] = (players[player]["position"] + d1 + d2) % 40

    tile = tiles.get(players[player]["position"])

    if tile == "chance":
        card = random.choice(chance_cards)
        messagebox.showinfo("✨ Chance", card[0])
        card[1](player)

    elif tile == "community":
        card = random.choice(community_cards)
        messagebox.showinfo("🎁 Community", card[0])
        card[1](player)

    elif tile == "gotojail":
        goto_jail(player)

    update_gui()
    next_turn()

window = tk.Tk()
window.title("🎀 Monopoly🎀 ")
window.geometry("500x420")
window.configure(bg="#ffe6f0")

current_label = tk.Label(window, font=("Arial", 14, "bold"), bg="#ffe6f0")
current_label.pack(pady=10)

info_box = tk.Text(window, height=10)
info_box.pack()

tk.Button(window, text="🎲 Roll Dice", bg="#ff99cc", fg="white", command=roll_action).pack(pady=6)
tk.Button(window, text="❌ Exit", bg="#ff66b2", fg="white", command=window.destroy).pack(pady=6)

update_gui()
window.mainloop()