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
                    with open("players.json", "w", encoding="utf-8") as f:
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
    
    print(f"Hello {username}! You are ready to play.")
    return False

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
            while True:
                if login(1):
                    break
        
        if key == '3':
            exit()
elif key == '2':
    cnt = 0
    while cnt < 4:
        while True:
            if login(2):
                break
        
        cnt += 1
elif key == '4':
    exit()