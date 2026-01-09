import re
import uuid
import json
import time
import os
import bcrypt
import curses
import pygame
from pathlib import Path

with open("users.json", "r") as f:
    try:
        users = json.load(f)
    except json.JSONDecodeError:
        users = {}

players = {}

pygame.mixer.init()
NAV_SOUND = pygame.mixer.Sound('menu_navigate_01.wav')
SELECT_SOUND = pygame.mixer.Sound('menu_select_00.wav')

def clean(t):
    time.sleep(t)
    os.system('cls' if os.name == 'nt' else 'clear')

def menu(options):
    def main(stdscr):
        curses.curs_set(0)
        stdscr.keypad(True)
        current = 0
        while True:
            stdscr.clear()
            for idx, option in enumerate(options):
                if idx == current:
                    stdscr.addstr(idx, 0, option, curses.A_REVERSE)
                else:
                    stdscr.addstr(idx, 0, option)
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_UP and current > 0:
                current -= 1
                NAV_SOUND.play()
            elif key == curses.KEY_DOWN and current < len(options) - 1:
                current += 1
                NAV_SOUND.play()
            elif key == curses.KEY_ENTER or key in [10, 13]:
                SELECT_SOUND.play()
                return options[current]
    return curses.wrapper(main)

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode("utf-8"), stored_hash.encode("utf-8"))

def signup(path):
    username = input("Enter your username: ")
    SELECT_SOUND.play()
    password = input("Enter your password: ")
    SELECT_SOUND.play()
    email = input("Enter your email: ")
    SELECT_SOUND.play()
    clean(0)
    
    for i in users:
        if users[i][0] == username:
            print("This username is already registered.")
            clean(1)
            return False
    
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if not re.match(pattern, email):
        print("This email is invalid.")
        clean(1)
        return False
    
    if len(password) < 8:
        print("Password length must be at least 8 characters.")
        clean(1)
        return False
    
    userid = str(uuid.uuid4())
    hpassword = hash_password(password)
    users[userid] = [username, hpassword, email]
    players[userid] = {
        "username": username,
        "password": hpassword,
        "position": 0,
        "cash": 1500,
        "broke": False,
        "jail": False,
        "get_out_of_jail_card": False,
        "dice_counter": 3,
        "property": {}
    }
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=4)
    
    print(f"Hello {username}! You are ready to play.")
    clean(1)
    return True

def login(path, Type):
    username = input("Enter your username: ")
    SELECT_SOUND.play()
    password = input("Enter your password: ")
    SELECT_SOUND.play()
    clean(0)
    
    check = False
    if Type == 1:
        for i in users:
            if users[i][0] == username:
                check = True
                if check_password(password, users[i][1]):
                    players[i] = {
                        "username": username,
                        "password": users[i][1],
                        "position": 0,
                        "cash": 1500,
                        "broke": False,
                        "jail": False,
                        "get_out_of_jail_card": False,
                        "dice_counter": 3,
                        "property": {}
                    }
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(players, f, ensure_ascii=False, indent=4)
                    print(f"Hello {username}! You are ready to play.")
                    clean(1)
                    return True
                break
    else:
        for i in players:
            if players[i]["username"] == username:
                check = True
                if check_password(password, players[i]["password"]):
                    print(f"Hello {username}! You are ready to play.")
                    clean(1)
                    return True
                break
    if check:
        print("The password is invalid.")
        clean(1)
    else:
        print("Username not found.")
        clean(1)
    return False

while True:
    choice = menu(["New Game", "Load Game", "Leaderboard", "Exit"])
    clean(0)
    
    if choice == "New Game":
        while True:
            game_name = input("Enter your game name: ") + ".json"
            SELECT_SOUND.play()
            clean(0)
            path = Path(__file__).parent / "old_games" / game_name
            if path.exists():
                print("This game already exists.")
                clean(1)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)
                players = {}
                break
        
        while len(players) < 4:
            sub_choice = menu(["Signup", "Login", "Back"])
            clean(0)
            if sub_choice == "Back":
                break
            elif sub_choice == "Signup":
                while not signup(path):
                    pass
            elif sub_choice == "Login":
                while not login(path, 1):
                    pass
        
        if len(players) == 4:
            break
    
    elif choice == "Load Game":
        game_name = input("Enter your game name: ") + ".json"
        SELECT_SOUND.play()
        clean(0)
        path = Path(__file__).parent / "old_games" / game_name
        if not path.exists():
            print("Game not found.")
            clean(1)
            continue
        with open(path, "r", encoding="utf-8") as f:
            players = json.load(f)
        
        if len(players) < 4:
            print(f"You have fewer than 4 players. {4 - len(players)} more people must register first.")
            clean(2)
            cnt = 4 - len(players)
            while cnt > 0:
                if signup(path):
                    cnt -= 1
            print("Now you can log in to your account to continue playing.")
            clean(2)
        
        for i in range(4):
            while not login(path, 2):
                pass
        
        break
    
    elif choice == "Exit":
        exit()