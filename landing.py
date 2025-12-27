import re
import json
import uuid

with open("users.json", "r") as f:
    try:
        users = json.load(f)
    except json.JSONDecodeError:
        users = {}

with open("players.json", "r") as f:
    try:
        players = json.load(f)
    except json.JSONDecodeError:
        players = {}

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
        "cash" : 120,
        "position" : 0,
        "property" : [],
        "jail" : False,
        "get_out_of_jail_card" : False,
        "dice_counter" : 3,
        "bankrupt" : False
    }
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
    with open("players.json", "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=4)
        
    print(f"Hello {username}! You are ready to play.")
    return True

print("1.New Game")
print("2.Load Game")
print("3.Leaderboard")
print("4.Exit")
key = input()

if key == '1':
    with open("players.json", "w", encoding="utf-8") as f:
        json.dump({}, f)
    
    with open("players.json", "r") as f:
        try:
            players = json.load(f)
        except json.JSONDecodeError:
            players = {}
    
    while len(players) <= 4:
        print("1.Singup")
        print("2.Login")
        print("3.Exit")
        key = input()
        
        if key == '1':
            while True:
                if signup():
                    break
        elif key == '2':
            pass
        
        if key == '3':
            exit()