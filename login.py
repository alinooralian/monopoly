import tkinter as tk
from tkinter import messagebox
import re
import uuid
import json

try:
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
except:
    users = {}

def save_users():
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def signup():
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    for u in users.values():
        if u["username"] == username:
            messagebox.showerror("💔 Error", "Username already exists")
            return

    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        messagebox.showerror("💔 Error", "Invalid email")
        return

    if len(password) < 8:
        messagebox.showerror("💔 Error", "Password too short")
        return

    uid = str(uuid.uuid4())

    users[uid] = {
        "username": username,
        "password": password,
        "email": email
    }

    save_users()
    messagebox.showinfo("🎉 Yay", "Signup successful 💖")

def login():
    username = username_entry.get()
    password = password_entry.get()

    for uid, u in users.items():
        if u["username"] == username and u["password"] == password:
            with open("current_player.json", "w", encoding="utf-8") as f:
                json.dump({"current_player": uid, "username": username}, f)

            messagebox.showinfo("✨ Welcome", f"Hi {username} 💕")
            window.destroy()

            import subprocess, sys
            subprocess.Popen([sys.executable, "game.py"])
            return

    messagebox.showerror("💔 Error", "Wrong username or password")

window = tk.Tk()
window.title("🎀 Monopoly Login 💖")
window.geometry("320x300")
window.configure(bg="#ffe6f0")

tk.Label(window, text="👤 Username", bg="#ffe6f0").pack()
username_entry = tk.Entry(window)
username_entry.pack()

tk.Label(window, text="🔒 Password", bg="#ffe6f0").pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

tk.Label(window, text="📧 Email (signup)", bg="#ffe6f0").pack()
email_entry = tk.Entry(window)
email_entry.pack()

tk.Button(window, text="✨ Signup", bg="#ff99cc", fg="white", command=signup).pack(pady=6)
tk.Button(window, text="💖 Login", bg="#ff66b2", fg="white", command=login).pack(pady=6)

window.mainloop()
