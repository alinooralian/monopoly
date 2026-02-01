import tkinter as tk
import subprocess
import sys

def run_signup():
    subprocess.Popen([sys.executable, "gui_func.py"])

def run_login():
    subprocess.Popen([sys.executable, "gui_func.py", "login"])

window = tk.Tk()
window.title("Monopoly")
window.geometry("300x250")
window.configure(bg="#FFDDEE")

tk.Label(
    window, 
    text="Monopoly Login", 
    bg="#FFDDEE", 
    fg="#FF69B4", 
    font=("Comic Sans MS", 16, "bold")
).pack(pady=15)

button_style = {
    "width": 15,
    "height": 2,
    "bg": "#FF99CC",
    "fg": "white",
    "font": ("Comic Sans MS", 12, "bold"),
    "relief": "raised",
    "bd": 3
}
tk.Button(window, text="Signup", command=run_signup, **button_style).pack(pady=5)
tk.Button(window, text="Login", command=run_login, **button_style).pack(pady=5)

tk.Button(window, text="Exit", command=window.destroy, **button_style).pack(pady=5)

window.mainloop()