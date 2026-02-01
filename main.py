import re
import uuid
import json
import time
import os
import shutil
import bcrypt
import curses
import pygame
import random
from pathlib import Path
from colorama import init, Fore, Back, Style
from rich.console import Console
from rich.table import Table

init()

with open("users.json", "r") as f:
    try:
        users = json.load(f)
    except json.JSONDecodeError:
        users = {}

palyers = {}

PLAYERS_COLORS={
    "P1" : Fore.RED,
    "P2" : Fore.BLUE,
    "P3" : Fore.GREEN,
    "P4" : Fore.YELLOW
}

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

def signup(path, num):
    username = input("Enter your username: ")
    SELECT_SOUND.play()
    password = input("Enter your password: ")
    SELECT_SOUND.play()
    email = input("Enter your email: ")
    SELECT_SOUND.play()
    clean(0)
    
    for i in users:
        if users[i][0] == username:
            print(Fore.RED + "This username is already registered." + Style.RESET_ALL)
            clean(2)
            return False
    
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if not re.match(pattern, email):
        print(Fore.RED + "This email is invalid." + Style.RESET_ALL)
        clean(2)
        return False
    
    if len(password) < 8:
        print(Fore.RED + "Password length must be at least 8 characters." + Style.RESET_ALL)
        clean(2)
        return False
    
    userid = str(uuid.uuid4())
    hpassword = hash_password(password)
    users[userid] = [username, hpassword, email]
    players[userid] = {
        "username": username,
        "password": hpassword,
        "is_bot": False,
        "color": PLAYERS_COLORS[f"P{num}"],
        "player_num": num,
        "position": 0,
        "cash": 1500,
        "jail": False,
        "get_out_of_jail_card": False,
        "dice_counter": 3,
        "property": {}
    }
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=4)
    
    print(PLAYERS_COLORS[f"P{players[userid]["player_num"]}"] + f"Hello {username}! You are ready to play." + Style.RESET_ALL)
    clean(2)
    return True

def login(path, num, Type):
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
                        "is_bot": False,
                        "color": PLAYERS_COLORS[f"P{num}"],
                        "player_num": num,
                        "position": 0,
                        "cash": 1500,
                        "jail": False,
                        "get_out_of_jail_card": False,
                        "dice_counter": 3,
                        "property": {}
                    }
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(players, f, ensure_ascii=False, indent=4)
                    print(PLAYERS_COLORS[f"P{players[i]["player_num"]}"] + f"Hello {username}! You are ready to play." + Style.RESET_ALL)
                    clean(2)
                    return True
                break
    else:
        for i in players.keys():
            if i == "bank" or i == "turn":
                continue
            if players[i]["username"] == username:
                check = True
                if check_password(password, players[i]["password"]):
                    print(PLAYERS_COLORS[f"P{players[i]["player_num"]}"] + f"Hello {username}! You are ready to play." + Style.RESET_ALL)
                    clean(2)
                    return True
                break
    if check:
        print(Fore.RED + "The password is invalid." + Style.RESET_ALL)
        clean(2)
    else:
        print(Fore.RED + "Username not found." + Style.RESET_ALL)
        clean(2)
    return False

def player_maker(cnt):
    usernames = ["Michael", "Nicholas", "Abraham", "Jacob"]
    while cnt:
        num = 5 - cnt
        userid = str(uuid.uuid4())
        username = usernames[cnt - 1]
        password = hash_password(usernames[cnt] + "2007")
        players[userid] = {
            "username": username,
            "password": password,
            "is_bot": True,
            "color": PLAYERS_COLORS[f"P{num}"],
            "player_num": num,
            "position": 0,
            "cash": 1500,
            "jail": False,
            "get_out_of_jail_card": False,
            "dice_counter": 3,
            "property": {}
        }
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
    
        cnt -= 1

    print(Fore.MAGENTA + "Bot players were created." + Style.RESET_ALL)
    clean(3)
        
def game(path):
    path_ = path / "tiles.json"
    with open(path_, "r", encoding="utf-8") as f:
            tiles = json.load(f)
    path__ = path / "tile_information.json"
    with open(path__, "r", encoding="utf-8") as f:
            tile_information = json.load(f)
    path___ = path
    path = path / f"{game_name}.json"
    
    def boardgame(pos):
        cell_width = 10
        
        p1, p2, p3, p4 = "P1", "P2", "P3", "P4"

        player_positions = {
            p1: pos[0],
            p2: pos[1],
            p3: pos[2],
            p4: pos[3]
        }

        def format_cell(players):
            plain = ' '.join(players)
            centered = plain.center(cell_width)

            for p in players:
                colored = PLAYERS_COLORS[p] + p + Style.RESET_ALL
                centered = centered.replace(p, colored, 1)

            return centered

        def get_players(cell_pos):
            players = [p for p, pp in player_positions.items() if pp == cell_pos]
            return format_cell(players)

        def print_horizontal_border(num_cells):
            return '+' + ('-' * cell_width + '+') * num_cells

        def print_line(content, num_cells):
            line = ''
            for i in range(num_cells):
                line += '|' + content[i].center(cell_width)
            line += '|'
            return line

        # Top side
        top_positions = list(range(20, 31))
        top_players = [get_players(i) for i in top_positions]
        print(print_horizontal_border(11))
        print(print_line(top_players, 11))
        print(print_horizontal_border(11))

        # Middle sides
        left_positions = list(reversed(range(11, 20)))
        right_positions = list(range(31, 40))
        left_players = [get_players(i) for i in left_positions]
        right_players = [get_players(i) for i in right_positions]

        total_width = cell_width * 11 + 12
        blank_space = total_width - 2 * (cell_width + 2)

        for i in range(9):
            border = '+' + '-' * cell_width + '+' + ' ' * blank_space + '+' + '-' * cell_width + '+'
            player_line = (
                '|' + left_players[i].center(cell_width) +
                '|' + ' ' * blank_space +
                '|' + right_players[i].center(cell_width) + '|'
            )

            print(border)
            print(player_line)
            print(border)

        # Bottom side
        bottom_positions = list(reversed(range(0, 11)))
        bottom_players = [get_players(i) for i in bottom_positions]
        print(print_horizontal_border(11))
        print(print_line(bottom_players, 11))
        print(print_horizontal_border(11))

    
    def jail_check(player_name): #check players jail status
        if players[player_name]["jail"] == True:
            in_jail(player_name) #player is in jail
        
        else:
            out_jail(player_name) #player is out of jail
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def in_jail(player_name):
        print(Fore.RED + "YOU ARE IN JAIL!" + Style.RESET_ALL)
        if players[player_name]["get_out_of_jail_card"] == True: #player has get out of jail chance card
            print(Fore.GREEN + "YOU HAVE 'GET OUT OF JAIL CHANCE CARD' " + Style.RESET_ALL)
            players[player_name]["get_out_of_jail_card"] = False
            players[player_name]["jail"] = False
            die1 , die2 = dice(player_name)
            if pair_dice(die1 , die2 , player_name) == True:
                move_to(player_name , die1 + die2)

        elif players[player_name]["dice_counter"] > 0: #player has option to roll dice to get out of jail
            if players[player_name]["is_bot"]:
                chosen_option = "1"
                print(Fore.YELLOW + "enter\n\t1.to roll dice\n\t2.to pay 50$\n" + Style.RESET_ALL)
                time.sleep(1)
                print("1\n")
            else:
                chosen_option = input(Fore.YELLOW + "enter\n\t1.to roll dice\n\t2.to pay 50$\n" + Style.RESET_ALL)
                SELECT_SOUND.play()
            if chosen_option == "1":
                roll_dice_jail(player_name)
            
            else: #player chose pay to get out of jail
                if pay(player_name , "bank" , 50 , "optional") == True: #if successful: get out of jail
                    players[player_name]["jail"] = False
                    players[player_name]["dice_counter"] = 3
                    die1 , die2 = dice(player_name)
                    if pair_dice(die1 , die2 , player_name) == True:
                        move_to(player_name , die1 + die2)  
                
                else: #roll dice
                    roll_dice_jail(player_name)
        
        else: #player should pay to get out of jail
            if pay(player_name , "bank" , 50 , "mandatory") == True:
                players[player_name]["jail"] = False
                players[player_name]["dice_counter"] = 3
                die1 , die2 = dice(player_name)
                if pair_dice(die1 , die2 , player_name) == True:
                    move_to(player_name , die1 + die2)
        with open(path, "w", encoding="utf-8") as f:
                json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def roll_dice_jail(player_name):
        die1 , die2 = dice(player_name)
        if die1 == die2: #dice are pair and get out of jail
            players[player_name]["jail"] = False
            players[player_name]["dice_counter"] = 3
            move_to(player_name , die1 + die2)
        
        else: #still stay in jail
            players[player_name]["dice_counter"] -= 1
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def out_jail(player_name):
        die1 , die2 = dice(player_name)
        if pair_dice(die1 , die2 , player_name) == True:
            move_to(player_name , die1 + die2)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def dice(player_name):
        if players[player_name]["is_bot"] == False:
            input(Fore.CYAN + "Press ENTER key for dice\n" + Style.RESET_ALL)
            SELECT_SOUND.play()
        die1 = random.randint(1 , 6)
        die2 = random.randint(1 , 6)
        print(f"YOUR DICE ARE: {die1} , {die2}")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)
        return die1 , die2


    def pair_dice(die1 , die2 , player_name):
        if die1 == die2:
            if double_dice_counter == 2:
                print(Fore.RED + "YOU ROLLED DOUBLES THREE TIMES IN A ROW, YOU GO TO JAIL!" + Style.RESET_ALL)
                gotojail(player_name)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(players, f, ensure_ascii=False, indent=4)
                with open(path_, "w", encoding="utf-8") as f:
                    json.dump(tiles, f, ensure_ascii=False, indent=4)
                with open(path__, "w", encoding="utf-8") as f:
                    json.dump(tile_information, f, ensure_ascii=False, indent=4)
                return False
            
            else:
                # global double_dice
                double_dice = True
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(players, f, ensure_ascii=False, indent=4)
                with open(path_, "w", encoding="utf-8") as f:
                    json.dump(tiles, f, ensure_ascii=False, indent=4)
                with open(path__, "w", encoding="utf-8") as f:
                    json.dump(tile_information, f, ensure_ascii=False, indent=4)
                return True

        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)
        return True


    def pay(debtor , creditor , value , status): #status can be mandatory or optional
        if players[debtor]["cash"] >= value:
            players[debtor]["cash"] -= value
            players[creditor]["cash"] += value
            print(Fore.GREEN + "your payment was successful" + Style.RESET_ALL)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(players, f, ensure_ascii=False, indent=4)
            with open(path_, "w", encoding="utf-8") as f:
                json.dump(tiles, f, ensure_ascii=False, indent=4)
            with open(path__, "w", encoding="utf-8") as f:
                json.dump(tile_information, f, ensure_ascii=False, indent=4)
            return True
        
        else:
            if status == "optional":
                print(Fore.RED + "you don't have enough money to pay" + Style.REST_ALL)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(players, f, ensure_ascii=False, indent=4)
                with open(path_, "w", encoding="utf-8") as f:
                    json.dump(tiles, f, ensure_ascii=False, indent=4)
                with open(path__, "w", encoding="utf-8") as f:
                    json.dump(tile_information, f, ensure_ascii=False, indent=4)
                return False
            
            while players[debtor]["cash"] < value:
                print(f"You are ${value - players[debtor]["cash"]} short.")
                if sell_property(debtor) == False: # player has gone broke
                    players[creditor]["cash"] += players[debtor]["cash"]
                    players[debtor]["cash"] = 0
                    player_list.remove(debtor)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def sell_property(player_name):
        if players[player_name]["property"] == {}:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(players, f, ensure_ascii=False, indent=4)
            with open(path_, "w", encoding="utf-8") as f:
                json.dump(tiles, f, ensure_ascii=False, indent=4)
            with open(path__, "w", encoding="utf-8") as f:
                json.dump(tile_information, f, ensure_ascii=False, indent=4)
            return False
        
        print(players[player_name]["property"])
        if players[player_name]["is_bot"]:
            bcp = random.ranint(0, len(players[player_name]["property"]) - 1)
            chosen_option = str(bcp)
            print(Fore.YELLOW + "enter the position of property you want to sell:\n" + Style.RESET_ALL)
            time.sleep(1)
            print(f"{str(bcp)}\n")
        else:
            chosen_option = input(Fore.YELLOW + "enter the position of property you want to sell:\n" + Style.RESET_ALL)
            SELECT_SOUND.play()
        players[player_name]["cash"] += sell_price(player_name , chosen_option)
        players[player_name]["property"].pop(chosen_option)
        tiles[chosen_option]["owner"] = "bank"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)
        return True


    def sell_price(player_name , pos):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)
        return (tile_information[str(pos)]["buy_price"] + (players[player_name]["property"][str(pos)] * tile_information[str(pos)]["house_price"])) // 2


    def move_to(player_name , step):
        if players[player_name]["position"] + step > 39: #get round reward
            players[player_name]["cash"] += 200
        
        players[player_name]["position"] = (players[player_name]["position"] + step) % 40
        print(f"YOUR CURRENT POSITION IS: {players[player_name]["position"]}")
        time.sleep(2)
        
        my_list = []
        for i in player_list:
            my_list.append(players[i]["position"])
        boardgame(my_list)
        time.sleep(2)
        
        tile_check(player_name , step)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def tile_check(player_name , step): #define tile's type and related function
        pos = players[player_name]["position"]
        if tiles[str(pos)]["type"] == "street":
            street(player_name , pos)
        
        elif tiles[str(pos)]["type"] == "community_chest":
            community_chest(player_name)
        
        elif tiles[str(pos)]["type"] == "tax":
            tax(player_name , pos)
        
        elif tiles[str(pos)]["type"] == "train":
            train(player_name , pos , "main")
        
        elif tiles[str(pos)]["type"] == "chance":
            chance(player_name)
        
        elif tiles[str(pos)]["type"] == "elctric/water":
            electric_water(player_name , pos , step , "main")
        
        elif tiles[str(pos)]["type"] == "gotojail":
            gotojail(player_name)
        
        else:
            pass
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def street(player_name , pos):
        print("YOU ARE IN A STREET!")
        if tiles[str(pos)]["owner"] == "bank":
            if players[player_name]["is_bot"]:
                chosen_option = "2"
                print(Fore.YELLOW + "enter\n\t1.to buy\n\t2.to pass\n" + Style.RESET_ALL)
                time.sleep(1)
                print("2\n")
            else:
                chosen_option = input(Fore.YELLOW + "enter\n\t1.to buy\n\t2.to pass\n" + Style.RESET_ALL)
                SELECT_SOUND.play()
            if chosen_option == "1":
                if pay(player_name , "bank" , tile_information[str(pos)]["buy_price"] , "optional") == True:
                    tiles[str(pos)]["owner"] = player_name
                    players[player_name]["property"][str(pos)] = 0
        
        elif tiles[str(pos)]["owner"] != player_name:
            print(Fore.RED + f"this street is for {players[tiles[str(pos)]["owner"]]["username"]}" + Style.RESET_ALL)
            pay(player_name , tiles[str(pos)]["owner"] , tile_information[str(pos)][str(players[tiles[str(pos)]["owner"]]["property"][str(pos)])] , "mandatory")\
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def build_house(player_name):
        if players[player_name]["property"] != {}:
            if players[player_name]["is_bot"]:
                chosen_option = "2"
                print(Fore.YELLOW + "enter\n\t1.to build a house\n\t2.to pass\n" + Style.RESET_ALL)
                time.sleep(1)
                print("2\n")
            else:
                chosen_option = input(Fore.YELLOW + "enter\n\t1.to build a house\n\t2.to pass\n" + Style.RESET_ALL)
                SELECT_SOUND.play()
            if chosen_option == "1":
                print(players[player_name]["property"])
                chosen_option = input(Fore.YELLOW + "enter the position of property you want to build a house:\n" + Style.RESET_ALL)
                SELECT_SOUND.play()
                if build_house_check(player_name , chosen_option) == True and players[player_name]["property"][chosen_option] != 5:
                    if pay(player_name , "bank" , tile_information[chosen_option]["house_price"] , "optional") == True:
                        players[player_name]["property"][chosen_option] += 1
                else:
                    print(Fore.RED + "YOU CAN'T BUILD A HOUSE HERE" + Style.RESET_ALL)
                    build_house(player_name)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def build_house_check(player_name , pos):
        color_owners = [tiles[i]["owner"] for i in color_index(tile_information[str(pos)]["color"])]
        if (color_owners.count(player_name) == len(color_owners)
            and players[player_name]["property"][str(pos)] == min([players[player_name]["property"][i] for i in color_owners]) ): 
            # if player owns all of the color and the stage of position is minimum
            with open(path, "w", encoding="utf-8") as f:
                json.dump(players, f, ensure_ascii=False, indent=4)
            with open(path_, "w", encoding="utf-8") as f:
                json.dump(tiles, f, ensure_ascii=False, indent=4)
            with open(path__, "w", encoding="utf-8") as f:
                json.dump(tile_information, f, ensure_ascii=False, indent=4)
            return True
        
        else:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(players, f, ensure_ascii=False, indent=4)
            with open(path_, "w", encoding="utf-8") as f:
                json.dump(tiles, f, ensure_ascii=False, indent=4)
            with open(path__, "w", encoding="utf-8") as f:
                json.dump(tile_information, f, ensure_ascii=False, indent=4)
            return False


    def color_index(color):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)
        return [x for x in tile_information if tiles[x]["type"] == "street" and tile_information[x].get("color" , False) == color]


    def community_chest(player_name):
        print(Fore.RED + "YOU ARE IN A COMMUNITY CHEST TILE!" + Style.RESET_ALL)
        community_card_coming(player_name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def tax(player_name , pos): #tax tiles
        if pos == 4:
            print(Fore.RED + "YOU ARE IN INCOME-TAX TILE!" + Style.RESET_ALL)
            pay(player_name , "bank" , 200 , "mandatory")
        
        elif pos == 38:
            print(Fore.RED + "YOU ARE IN LUXURY-TAX TILE!" + Style.RESET_ALL)
            pay(player_name , "bank" , 100 , "mandatory")
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def train(player_name , pos , status): #train stations / status can be main or chance
        print(Fore.YELLOW + "YOU ARE IN A TRAIN STATION!" + Style.RESET_ALL)
        if tiles[str(pos)]["owner"] != "bank" and tiles[str(pos)]["owner"] != player_name:
            print(Fore.RED + f"this train station is for {tiles[str(pos)]["owner"]}" + Style.RESET_ALL)
            if status == "main":
                pay(player_name , tiles[str(pos)]["owner"] , 25 * (2 ** (train_own_count(tiles[str(pos)]["owner"]) - 1)) , "mandatory")
            else:
                pay(player_name , tiles[str(pos)]["owner"] , 50 * (2 ** (train_own_count(tiles[str(pos)]["owner"]) - 1)) , "mandatory")
        
        elif tiles[str(pos)]["owner"] == "bank":
            if players[player_name]["is_bot"]:
                chosen_option = "2"
                print(Fore.YELLOW + "enter\n\t1.to buy\n\t2.to pass\n" + Style.RESET_ALL)
                time.sleep(1)
                print("2\n")
            else:
                chosen_option = input(Fore.YELLOW + "enter\n\t1.to buy\n\t2.to pass\n" + Style.RESET_ALL)
                SELECT_SOUND.play()
            if chosen_option == "1":
                if pay(player_name , "bank" , 200 , "optional") == True:
                    tiles[str(pos)]["owner"] = player_name
                    players[player_name]["property"][str(pos)] = None
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)
            

    def train_own_count(owner): #count how many stations owner got
        owners = [tiles[i]["owner"] for i in [5 , 15 , 25 , 35]]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)
        return owners.count(owner)


    def chance(player_name):
        print(Fore.GREEN + "YOU ARE IN A CHANCE TILE!" + Style.RESET_ALL)
        chance_card_coming(player_name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def electric_water(player_name , pos , step , status): #electric company and water works / status can be main or chance
        print(Fore.YELLOW + "YOU ARE IN A UTILITY TILE!" + Style.RESET_ALL)
        if tiles[str(pos)]["owner"] != "bank" and tiles[str(pos)]["owner"] != player_name:
            print(Fore.RED + f"this utility is for {tiles[str(pos)]["owner"]}" + Style.RESET_ALL)
            if status == "main":
                if tiles[str(pos)]["owner"] == tiles[switch_electric_water(pos)]["owner"]:
                    pay(player_name , tiles[str(pos)]["owner"] , 10 * step , "mandatory")
                
                else:
                    pay(player_name , tiles[str(pos)]["owner"] , 4 * step , "mandatory")   

            else:
                die1 , die2 = dice(player_name)
                pay(player_name , tiles[str(pos)]["owner"] , 10 * (die1 + die2) , "mandatory")

        elif tiles[str(pos)]["owner"] == "bank":
            if players[player_name]["is_bot"]:
                chosen_option = "2"
                print(Fore.YELLOW + "enter\n\t1.to buy\n\t2.to pass\n" + Style.RESET_ALL)
                time.sleep(1)
                print("2\n")
            else:
                chosen_option = input(Fore.YELLOW + "enter\n\t1.to buy\n\t2.to pass\n" + Style.RESET_ALL)
                SELECT_SOUND.play()
            if chosen_option == "1":
                if pay(player_name , "bank" , 150 , "optional") == True:
                    tiles[str(pos)]["owner"] = player_name
                    players[player_name]["property"][str(pos)] = None
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)
            

    def switch_electric_water(pos): #switches between electric company and water works
        if pos == 12: #electric company position
            return 28
        
        elif pos == 28: #water works position
            return 12
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)

    def gotojail(player_name): #go to jail tile
        print(Fore.RED + "YOU GO TO JAIL!" + Style.RESET_ALL)
        players[player_name]["jail"] = True
        players[player_name]["position"] = 10 # jail position
        # global double_dice
        double_dice = False
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)



    #chance card functions:

    def advance_to(player_name , pos):
        if players[player_name]["position"] > pos:
            players[player_name]["cash"] += 200
        players[player_name]["position"] = pos
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def nearest_railroad(player_name):
        station = ((players[player_name]["position"] // 10) * 10) + 5
        players[player_name]["position"] = station
        train(player_name , station , "chance")
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def nearest_utility(player_name):
        if players[player_name]["position"] < 20:
            utility = 12
        else:
            utility = 28
        players[player_name]["position"] = utility
        electric_water(player_name , utility , 0 , "chance")
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def give_jail_card(player_name):
        players[player_name]["get_out_of_jail_card"] = True
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def pay_per_house(player_name , house , hotel):
        cost = 0
        for stage in players[player_name]["property"].values():
            if stage == 5:
                cost += (hotel + (4 * house))
            else:
                cost += (stage * house)
        
        pay(player_name , "bank" , cost , "mandatory")
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def pay_each_player(player_name):
        for p in player_list:
            pay(player_name , p , 50 , "mandatory")
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def collect_each_player(player_name):
        for p in player_list:
            pay(p , player_name , 10 , "mandatory")
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)




    def chance_card_coming(player_name):
        card = random.choice(chance_cards)
        print("🎲 Chance:", card["text"])
        card["action"](player_name)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    def community_card_coming(player_name):
        card = random.choice(community_chest_cards)
        print("📦 Community Chest:", card["text"])
        card["action"](player_name)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=4)
        with open(path_, "w", encoding="utf-8") as f:
            json.dump(tiles, f, ensure_ascii=False, indent=4)
        with open(path__, "w", encoding="utf-8") as f:
            json.dump(tile_information, f, ensure_ascii=False, indent=4)


    chance_cards = [
        {"text": "Advance to Boardwalk"                                                                                             , "action": lambda player_name: advance_to(player_name, 39)} ,
        {"text": "Advance to Go - Collect $200"                                                                                     , "action": lambda player_name: advance_to(player_name, 0)} ,
        {"text": "Advance to Illinois Avenue - if you pass Go, Collect $200"                                                        , "action": lambda player_name: advance_to(player_name, 24)} ,
        {"text": "Advance to St. Charles Place - if you pass Go, Collect $200"                                                      , "action": lambda player_name: advance_to(player_name, 11)} ,
        {"text": "Advance to nearest Railroad - if unowned, you may buy it; if owned, pay twice the rent"                           , "action": lambda player_name: nearest_railroad(player_name)} ,
        {"text": "Advance to nearest Utility - if unowned, you may buy it; if owned, roll dice and pay owner 10* the amount thrown" , "action": lambda player_name: nearest_utility(player_name)} ,
        {"text": "Bank pays you dividend of $50"                                                                                    , "action": lambda player_name: pay("bank" , player_name , 50 , "mandatory")} ,
        {"text": "Get Out of Jail Free"                                                                                             , "action": lambda player_name: give_jail_card(player_name)} ,
        {"text": "Go Back 3 Spaces"                                                                                                 , "action": lambda player_name: move_to(player_name , -3)} ,
        {"text": "Go to Jail"                                                                                                       , "action": lambda player_name: gotojail(player_name)} ,  
        {"text": "Make general repairs on all your property - For each house pay $25; for each hotel pay $100"                      , "action": lambda player_name: pay_per_house(player_name , house = 25 , hotel = 100)} ,
        {"text": "Speeding fine $15"                                                                                                , "action": lambda player_name: pay(player_name , "bank" , 15 , "mandatory")} , 
        {"text": "Take a trip to Reading Railroad"                                                                                  , "action": lambda player_name: advance_to(player_name , 5)} ,
        {"text": "You have been elected Chairman of the Board - pay each player $50"                                                , "action": lambda player_name: pay_each_player(player_name)} ,
        {"text": "Your building loan matures - Receive $150"                                                                        , "action": lambda player_name: pay("bank" , player_name , 150 , "mandatory")}
    ]


    community_chest_cards = [
        {"text": "Advance to Go"                                                              , "action": lambda player_name: advance_to(player_name , 0)} ,
        {"text": "Bank error in your favor - Collect $200"                                    , "action": lambda player_name: pay("bank" , player_name , 200 , "mandatory")} ,
        {"text": "Doctor's fee - Pay $50"                                                     , "action": lambda player_name: pay(player_name, "bank" , 50 , "mandatory")} ,
        {"text": "From sale of stock you get $50"                                             , "action": lambda player_name: pay("bank" , player_name , 50 , "mandatory")} ,
        {"text": "Get Out of Jail Free"                                                       , "action": lambda player_name: give_jail_card(player_name)} ,
        {"text": "Go to Jail"                                                                 , "action": lambda player_name: gotojail(player_name)} ,
        {"text": "Holiday fund matures - Receive $100"                                        , "action": lambda player_name: pay("bank" , player_name , 100 , "mandatory")} ,
        {"text": "Income tax refund - Collect $20"                                            , "action": lambda player_name: pay("bank" , player_name , 20 , "mandatory")} ,
        {"text": "It is your birthday - Collect $10 from every player"                        , "action": lambda player_name: collect_each_player(player_name)} ,
        {"text": "Life insurance matures - Collect $100"                                      , "action": lambda player_name: pay("bank" , player_name , 100 , "mandatory")} ,
        {"text": "Pay hospital fees of $100"                                                  , "action": lambda player_name: pay(player_name , "bank" , 100 , "mandatory")} ,
        {"text": "Pay school fees of $50"                                                     , "action": lambda player_name: pay(player_name , "bank" , 50 , "mandatory")} ,
        {"text": "Receive $25 consultancy fee"                                                , "action": lambda player_name: pay("bank" , player_name , 25 , "mandatory")} ,
        {"text": "You are assessed for street repairs - Pay $40 per house and $115 per hotel" , "action": lambda player_name: pay_per_house(player_name, house = 40, hotel = 115)} ,
        {"text": "You have won second prize in a beauty contest - Collect $10"                , "action": lambda player_name: pay("bank" , player_name , 10 , "mandatory")} ,
        {"text": "You inherit $100"                                                           , "action": lambda player_name: pay("bank" , player_name , 100 , "mandatory")}
    ]

    def print_player(id):
        print(players[id]["color"] + f"{players[id]["username"]} -> p{players[id]["player_num"]}: " + Style.RESET_ALL)
        print(f"    Position: {players[id]["position"]}")
        print(f"    Cash: {players[id]["cash"]}")
        print(f"    Jail: {players[id]["jail"]}")
        print(f"    Get out of jail card: {players[id]["get_out_of_jail_card"]}")
        print(f"    Dice Counter: {players[id]["dice_counter"]}")
        print(f"    Property: {players[id]["property"]}")
        print()

    player_list = list(players.keys())
    player_list.remove("bank")
    player_list.remove("turn")
    player_list.remove("real_player")
    player = players["turn"]
    double_dice_counter = 0

    while len(player_list) > 1:
        print_player(player)
        double_dice = False
        build_house(player)
        jail_check(player)
        if double_dice == False:
            player = player_list[(player_list.index(player) + 1) % len(player_list)]
            players["turn"] = player
            
            with open(path, "w", encoding="utf-8") as f:
                json.dump(players, f, ensure_ascii=False, indent=4)

            double_dice_counter = 0
        else:
            double_dice_counter += 1
        
        time.sleep(3)
        
        print("\n\n\n\n")
        
        console = Console()

        table = Table(title=Fore.GREEN + "Scoreboard" + Style.RESET_ALL, style="magenta")

        table.add_column("ID", justify="cneter", no_wrap=False)
        table.add_column("Name", justify="center", no_wrap=False)
        table.add_column("Position", justify="center", no_wrap=False)
        table.add_column("Cash", justify="center", no_wrap=False)
        table.add_column("Jail", justify="center", no_wrap=False)
        table.add_column("Get out of jail card", justify="center", no_wrap=False)
        table.add_column("Dice Counter", justify="center", no_wrap=False)
        table.add_column("Property", justify="center", no_wrap=False)

        colors = ["red", "blue", "green", "yellow"]
        cnt = 0
        for id in player_list:
            table.add_row(f"P{str(players[id]["player_num"])}", str(players[id]["username"]), str(players[id]["position"]), str(players[id]["cash"]), str(players[id]["jail"]), str(players[id]["get_out_of_jail_card"]), str(players[id]["dice_counter"]), str(players[id]["property"]), style=colors[cnt])
            cnt += 1

        console.print(table)
        
        time.sleep(5)
        
        print("\n\n\n\n")
        
        input(Fore.CYAN + "Press ENTER to next round\n" + Style.RESET_ALL)
        SELECT_SOUND.play()
        clean(3)

    print(Fore.GREEN + f"Wow! {players[player_list[0]]["username"]} -> P{players[player_list[0]]["player_num"]} won this game." + Style.RESET_ALL)
    clean(5)
    
    with open("leaderboard.json", "r") as f:
        try:
            leaderboard = json.load(f)
        except:
            leaderboard = {}

    if player_list[0] not in leaderboard.keys():
        leaderboard[player_list[0]] = {
            "username" : players[player_list[0]]["username"],
            "win_count" : 1,
            "money" : players[player_list[0]]["cash"],
            "games" : [game_name]
        }
    else:
        leaderboard[player_list[0]]["win_count"] += 1
        leaderboard[player_list[0]]["money"] = max(players[player_list[0]]["cash"], leaderboard[player_list[0]]["money"])
        leaderboard[player_list[0]]["games"].append(game_name)
    with open("leaderboard.json", "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=4)
    
    with open("leaderboard.json", "r", encoding="utf-8") as f:
        info = json.load(f)

    console = Console()


    table = Table(title=Fore.GREEN + "Leaderboard" + Style.RESET_ALL, style="magenta")

    table.add_column("Rate", justify="cneter", no_wrap=False)
    table.add_column("Name", justify="center", no_wrap=False)
    table.add_column("Wins", justify="center", no_wrap=False)
    table.add_column("Maximum Money", justify="center", no_wrap=False)
    table.add_column("Game", justify="center", no_wrap=False)

    row = []
    for key in info.keys():
        row.append((info[key]["win_count"], info[key]["money"], info[key]["username"], info[key]["games"]))

    leaderboard = sorted(row, reverse=True)

    for R, i in enumerate(leaderboard, 1):
        if R == 1:
            table.add_row(str(R), str(i[2]), str(i[0]), str(i[1]), str(i[3]), style="bold yellow")
        elif R == 2:
            table.add_row(str(R), str(i[2]), str(i[0]), str(i[1]), str(i[3]), style="bold white")
        elif R == 3:
            table.add_row(str(R), str(i[2]), str(i[0]), str(i[1]), str(i[3]), style="bold red")
        else:
            table.add_row(str(R), str(i[2]), str(i[0]), str(i[1]), str(i[3]))

    console.print(table)
    
    input(Fore.RED + "Press ENTER for exit\n" + Style.RESET_ALL)
    SELECT_SOUND.play()
    
    os.remove(path)
    os.remove(path_)
    os.remove(path__)
    os.rmdir(path___)

    exit()

pth = Path(__file__).parent / "old_games"
if not pth.exists():
    os.mkdir(Path(__file__).parent / "old_games")

while True:
    choice = menu(["New Game", "Load Game", "Leaderboard", "About Monopoly", "About Us", "Exit"])
    clean(0)
    
    if choice == "New Game":
        while True:
            game_name = input("Enter your game name: ")
            SELECT_SOUND.play()
            clean(0)
            path = Path(__file__).parent / "old_games" / game_name / f"{game_name}.json"
            if path.exists():
                print(Fore.RED + "This game already exists." + Style.RESET_ALL)
                clean(1)
            else:
                os.mkdir(Path(__file__).parent / "old_games" / game_name)
                shutil.copy(os.path.join(os.getcwd(), "tiles.json"), Path(__file__).parent / "old_games"/ game_name)
                shutil.copy(os.path.join(os.getcwd(), "tile_information.json"), Path(__file__).parent / "old_games"/ game_name)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)
                players = {}
                break
        RP = int(input("Enter the number of players: "))
        SELECT_SOUND.play()
        clean(0)
        cnt = 1
        CHECK = False
        while len(players) < RP:
            sub_choice = menu(["Signup", "Login", "Back"])
            clean(0)
            if sub_choice == "Back":
                CHECK = True
                break
            elif sub_choice == "Signup":
                while not signup(path, cnt):
                    pass
            elif sub_choice == "Login":
                while not login(path, cnt, 1):
                    pass
            cnt += 1
        
        if not CHECK:
            player_maker(4 - RP)
        
        if len(players) == 4:
            players["bank"] = {
                "cash" : float(1e18)
            }
            p = list(players.keys())
            players["turn"] = p[0]
            players["real_player"] = RP
            with open(path, "w", encoding="utf-8") as f:
                json.dump(players, f, ensure_ascii=False, indent=4)
            path = Path(__file__).parent / "old_games" / game_name
            game(path)
            break
    elif choice == "Load Game":
        game_name = input("Enter your game name: ")
        SELECT_SOUND.play()
        clean(0)
        path = Path(__file__).parent / "old_games" / game_name / f"{game_name}.json"
        if not path.exists():
            print(Fore.RED + "Game not found." + Style.RESET_ALL)
            clean(1)
            continue
        with open(path, "r", encoding="utf-8") as f:
            players = json.load(f)
        
        cnt = len(players)
        if cnt == 7:
            cnt = players["real_player"]
            print(Fore.YELLOW + f"Your number of non-bot players is {cnt}." + Style.RESET_ALL)
            clean(2)
            while cnt:
                while not login(path, cnt, 2):
                    pass
                cnt -= 1
            path = Path(__file__).parent / "old_games" / game_name
            game(path)
            break

        print(Fore.YELLOW + f"First, {cnt} players must log in to their accounts." + Style.RESET_ALL)
        clean(3)
        while cnt:
            while not login(path, cnt, 2):
                pass
            cnt -= 1
        RP = int(input("Enter the number of players: "))
        SELECT_SOUND.play()
        clean(0)
        cnt = RP - len(players)
        print(Fore.YELLOW + f"Now you need to add {cnt} more players to this game." + Style.RESET_ALL)
        clean(3)
        i = len(players) + 1
        CHECK = False
        while cnt:
            sub_choice = menu(["Signup", "Login", "Back"])
            clean(0)
            if sub_choice == "Back":
                CHECK = True
                break
            elif sub_choice == "Signup":
                while not signup(path, i):
                    pass
            elif sub_choice == "Login":
                while not login(path, i, 1):
                    pass
            cnt -= 1
            i += 1
        
        if not CHECK:
            player_maker(4 - RP)

        if len(players) == 4:
            players["bank"] = {
                "cash" : float(1e18)
            }
            p = list(players.keys())
            players["turn"] = p[0]
            players["real_player"] = RP
            with open(path, "w", encoding="utf-8") as f:
                json.dump(players, f, ensure_ascii=False, indent=4)
            path = Path(__file__).parent / "old_games" / game_name
            game(path)
            break
    elif choice == "Leaderboard":
        with open("leaderboard.json", "r", encoding="utf-8") as f:
            info = json.load(f)
        
        if len(info) == 0:
            print(Fore.RED + "There is no finished game." + Style.RESET_ALL)
            print("\n\n\n")
            input(Fore.CYAN + "Press ENTER for return\n" + Style.RESET_ALL)
            SELECT_SOUND.play()
        else:

            console = Console()

            table = Table(title=Fore.GREEN + "Leaderboard" + Style.RESET_ALL, style="magenta")

            table.add_column("Rate", justify="cneter", no_wrap=False)
            table.add_column("Name", justify="center", no_wrap=False)
            table.add_column("Wins", justify="center", no_wrap=False)
            table.add_column("Maximum Money", justify="center", no_wrap=False)
            table.add_column("Game", justify="center", no_wrap=False)

            row = []
            for key in info.keys():
                row.append((info[key]["win_count"], info[key]["money"], info[key]["username"], info[key]["games"]))

            leaderboard = sorted(row, reverse=True)

            for R, i in enumerate(leaderboard, 1):
                if R == 1:
                    table.add_row(str(R), str(i[2]), str(i[0]), str(i[1]), str(i[3]), style="bold yellow")
                elif R == 2:
                    table.add_row(str(R), str(i[2]), str(i[0]), str(i[1]), str(i[3]), style="bold white")
                elif R == 3:
                    table.add_row(str(R), str(i[2]), str(i[0]), str(i[1]), str(i[3]), style="bold red")
                else:
                    table.add_row(str(R), str(i[2]), str(i[0]), str(i[1]), str(i[3]))

            console.print(table)
            
            input(Fore.CYAN + "Press ENTER for return\n" + Style.RESET_ALL)
            SELECT_SOUND.play()
    elif choice == "About Monopoly":
        print(Fore.YELLOW + "Introduction and Description of the Monopoly Game" + Style.RESET_ALL)
        print("Monopoly is a classic economic and strategic board game that challenges players’ skills in money management, strategic decision-making, and risk-taking. In this game, each player takes on the role of an investor entering a city filled with streets, properties, and business opportunities. The main objective is to buy properties, develop them with houses and hotels, collect rent, and ultimately bankrupt your opponents.")
        print(Fore.YELLOW + "Gameplay and Atmosphere" + Style.RESET_ALL)
        print("Players move around the board by rolling dice. Depending on the space they land on, they may:")
        print("Purchase a street or property")
        print("Pay rent to another player")
        print("Draw a Chance or Community Chest card")
        print("Or be sent to Jail")
        print("Every financial decision can drastically change the course of the game.A smart investment may turn you into the wealthiest player, while a single mistake can lead to bankruptcy.")
        print(Fore.YELLOW + "Ultimate Goal of the Game" + Style.RESET_ALL)
        print("The winner is the player who, through smart financial management and strategic asset control, eliminates all other players financially and becomes the sole owner of the city.")
        print("\n\n\n")
        input(Fore.CYAN + "Press ENTER for return.\n" + Style.RESET_ALL)
        SELECT_SOUND.play()
    elif choice == "About Us":
        print("This project is the result of a group collaboration that was programmed and developed by the G4 group for the BP lesson.")
        print("The members of this group include:\n\n")
        print(Fore.MAGENTA + "Mehshid Aryan")
        print("Mahbanoo Javanmardi")
        print("Mana Najarsharifi")
        print("Ali Salehi")
        print("Sowgol Safari")
        print("and Ali Nooralian." + Style.RESET_ALL)
        print("\n\n")
        print(Fore.YELLOW + "We hope you will have a sweet experience with this game." + Style.RESET_ALL)
        print("\n\n\n")
        input(Fore.CYAN + "Press ENTER for return.\n" + Style.RESET_ALL)
        SELECT_SOUND.play()
    elif choice == "Exit":
        exit()