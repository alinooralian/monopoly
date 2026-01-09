import re
import uuid
import json
import time
import os
from pathlib import Path

with open("users.json", "r") as f:
    try:
        users = json.load(f)
    except json.JSONDecodeError:
        users = {}

players = dict()

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
    users[userid] = [username, password, email]
    players[userid] = {
        "username" : username,
        "password" : password,
        "money" : 120,
        "property" : 0,
        "prsion" : False
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
                if users[i][1] == password:
                    players[i] = {
                        "username" : username,
                        "password" : password,
                        "money" : 120,
                        "property" : 0,
                        "prsion" : False
                    }
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(players, f, ensure_ascii=False, indent=4)
                    return True
                break
    else:
        for i in players:
            if players[i]["username"] == username:
                check = True
                if players[i]["password"] == password:
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
    game_name = input("Enter your game name: ") + ".json"
    path = Path(__file__).parent / "old_games" / game_name
    
    with open(path, "x", encoding="utf-8") as f:
        pass
    
    with open(path, "r", encoding="utf-8") as f:
        try:
            players = json.load(f)
        except json.JSONDecodeError:
            players = {}
    
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