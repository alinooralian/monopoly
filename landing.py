import re
import uuid
import json
import time
import os
import bcrypt
from pathlib import Path

with open("users.json", "r") as f:
    try:
        users = json.load(f)
    except json.JSONDecodeError:
        users = {}

players = dict()

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode("utf-8"), stored_hash.encode("utf-8"))

def signup():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    email = input("Enter your email: ")
    
    for i in users:
        if users[i][0] == username:
            print("This username is already registered.")
            return False
    
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if not re.match(pattern, email):
        print("This email is invalid.")
        return False
    
    if len(password) < 8:
        print("Password length must be at least 8 characters.")
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
    return True

def login(Type):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    check = False
    if Type == 1:
        for i in users:
            if users[i][0] == username:
                check = True
                if check_password(password, users[i][1]):
                    players[i] = {
                        "username": username,
                        "password": hash_password(password),
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
                    return True
                break
    else:
        for i in players:
            if players[i]["username"] == username:
                check = True
                if check_password(password, players[i]["password"]):
                    return True
    if check:
        print("The password is invalid.")
    else:
        print("Username not found.")
    
    return False


print("1.New Game")
print("2.Load Game")
print("3.Leaderboard")
print("4.Exit")
key = input()

if key == '1':
    while True:
        game_name = input("Enter your game name: ") + ".json"
        path = Path(__file__).parent / "old_games" / game_name
        if path.exists():
            print("This game already exists.")
        else:
            with open(path, "w", encoding="utf-8") as f:
                pass
            
            with open(path, "r", encoding="utf-8") as f:
                try:
                    players = json.load(f)
                except json.JSONDecodeError:
                    players = {}
            break
    
    while True:
        if len(players) >= 4:
            break
        print("1.Singup")
        print("2.Login")
        print("3.Exit")
        key = input()
        
        if key == '1':
            while True:
                if signup():
                    break
        
        if key == '2':
            while True:
                if login(1):
                    break
        
        if key == '3':
            exit()

elif key == '2':
    game_name = input("Enter your game name: ") + ".json"
    path = Path(__file__).parent / "old_games" / game_name

    with open(path, "r", encoding="utf-8") as f:
        try:
            players = json.load(f)
        except json.JSONDecodeError:
            players = {}

    if len(players) < 4:
        print(f"You have fewer than 4 players. {4 - len(players)} more people must register first.")

        while len(players) < 4:
            while True:
                if signup():
                    break
        
        print("Now you can log in to your account to continue playing.")

    cnt = 0
    while cnt < 4:
        while True:
            if login(2):
                break
        
        cnt += 1
elif key == '4':
    exit()