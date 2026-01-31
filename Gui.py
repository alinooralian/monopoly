import tkinter as tk
from tkinter import messagebox
import re
import uuid
import json

try:
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    users = {}

try:
    with open("players.json", "r", encoding="utf-8") as f:
        players = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    players = {}

def signup():
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    for i in users:
        if users[i][0] == username:
            return False, "This username is already registered."
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if not re.match(pattern, email):
        return False, "This email is invalid."
    if len(password) < 8:
        return False, "Password length must be at least 8 characters."
    userid = str(uuid.uuid4())
    users[userid] = [username, password, email]
    players[userid] = {
        "username": username,
        "password": password,
        "money": 120,
        "property": 0,
        "prsion": False
    }
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
    with open("players.json", "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=4)
    return True, "Signup successful!"

def login(Type):
    username = username_entry.get()
    password = password_entry.get()
    check = False
    if Type == 1:
        for i in users:
            if users[i][0] == username:
                check = True
                if users[i][1] == password:
                    players[i] = {
                        "username": username,
                        "password": password,
                        "money": 120,
                        "property": 0,
                        "prsion": False
                    }
                    with open("players.json", "w", encoding="utf-8") as f:
                        json.dump(players, f, ensure_ascii=False, indent=4)
                    return True, "Login successful!"
                break
    else:
        for i in players:
            if players[i]["username"] == username:
                check = True
                if players[i]["password"] == password:
                    return True, "Login successful!"
    if check:
        return False, "The password is invalid."
    else:
        return False, "Username not found."

window = tk.Tk()
window.title("🎀 Monopoly 🎀")
window.geometry("320x370")
window.configure(bg="#FFF0F5")

header_font = ("Comic Sans MS", 18, "bold")
label_font = ("Comic Sans MS", 12, "bold")
entry_font = ("Comic Sans MS", 11)
button_font = ("Comic Sans MS", 12, "bold")

tk.Label(window, text="🎀 Monopoly Login 🎀", bg="#FFF0F5", fg="#FF69B4", font=header_font).pack(pady=15)
button_style = {
    "width": 18,
    "height": 2,
    "bg": "#FFB6C1",
    "fg": "white",
    "font": button_font,
    "relief": "raised",
    "bd": 4
}

def open_signup_window():
    global username_entry, password_entry, email_entry
    signup_win = tk.Toplevel(window)
    signup_win.title("Signup")
    signup_win.geometry("300x280")
    signup_win.configure(bg="#FFF0F5")
    tk.Label(signup_win, text="Username:", bg="#FFF0F5", fg="#C71585", font=label_font).pack(pady=2)
    username_entry = tk.Entry(signup_win, font=entry_font)
    username_entry.pack(pady=2)
    tk.Label(signup_win, text="Password:", bg="#FFF0F5", fg="#C71585", font=label_font).pack(pady=2)
    password_entry = tk.Entry(signup_win, show="*", font=entry_font)
    password_entry.pack(pady=2)
    tk.Label(signup_win, text="Email:", bg="#FFF0F5", fg="#C71585", font=label_font).pack(pady=2)
    email_entry = tk.Entry(signup_win, font=entry_font)
    email_entry.pack(pady=2)
    def submit():
        if len(players) >= 4:
            messagebox.showinfo("Signup", "Maximum 4 players allowed.")
            return
        ok, msg = signup()
        messagebox.showinfo("Signup", msg)
        if ok:
            signup_win.destroy()
    tk.Button(signup_win, text="Submit", command=submit, **button_style).pack(pady=10)

def open_login_window(Type=1):
    global username_entry, password_entry
    login_win = tk.Toplevel(window)
    login_win.title("Login")
    login_win.geometry("300x220")
    login_win.configure(bg="#FFF0F5")
    tk.Label(login_win, text="Username:", bg="#FFF0F5", fg="#C71585", font=label_font).pack(pady=2)
    username_entry = tk.Entry(login_win, font=entry_font)
    username_entry.pack(pady=2)
    tk.Label(login_win, text="Password:", bg="#FFF0F5", fg="#C71585", font=label_font).pack(pady=2)
    password_entry = tk.Entry(login_win, show="*", font=entry_font)
    password_entry.pack(pady=2)
    def submit():
        ok, msg = login(Type)
        messagebox.showinfo("Login", msg)
        if ok:
            login_win.destroy()
    tk.Button(login_win, text="Submit", command=submit, **button_style).pack(pady=10)

tk.Button(window, text="Signup", command=open_signup_window, **button_style).pack(pady=5)
tk.Button(window, text="Login", command=lambda: open_login_window(1), **button_style).pack(pady=5)
tk.Button(window, text="Exit", command=window.destroy, **button_style).pack(pady=5)

window.mainloop()