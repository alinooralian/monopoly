def jail_check(player_name): #check players jail status
    if players[player_name]["jail"] == True:
        in_jail(player_name) #player is in jail
    else:
        out_jail(player_name) #player is out of jail

def in_jail(player_name):
    print("YOU ARE IN JAIL!")
    if players[player_name]["get_out_of_jail_card"] == True: #player has get out of jail chance card
        print("YOU HAVE 'GET OUT OF JAIL CHANCE CARD' ")
        players[player_name]["get_out_of_jail_card"] = False
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!# card gets back to chance cards
        players[player_name]["jail"] = False
        dice1 , dice2 = dice()
        if pair_dice(dice1 , dice2 , player_name) == True:
            move_to(player_name , dice1 + dice2)

    elif players[player_name]["dice_counter"] > 0: #player has option to roll dice to get out of jail
        chosen_option = input("enter\n\t1.to roll dice\n\t2.to pay 50$\n")
        if chosen_option == "1":
            dice1 , dice2 = dice()
            if dice1 == dice2: #dices are pair and get out of jail
                players[player_name]["jail"] = False
                players[player_name]["dice_counter"] = 3
                move_to(player_name , dice1 + dice2)
            else: #still stay in jail
                players[player_name]["dice_counter"] -= 1
        else: #player chose pay to get out of jail
            pay(player_name , "bank" , 50 , "mandatory")    #if successful: get out of jail / else: go to roll dice part !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    else: #player should pay to get out of jail
        if pay(player_name , "bank" , 50 , "mandatory") == True:
            players[player_name]["jail"] = False
            players[player_name]["dice_counter"] = 3
            dice1 , dice2 = dice()
            if pair_dice(dice1 , dice2 , player_name) == True:
                move_to(player_name , dice1 + dice2)

def out_jail(player_name):
    dice1 , dice2 = dice()
    if pair_dice(dice1 , dice2 , player_name) == True:
        move_to(player_name , dice1 + dice2)

def dice():
    dice1 = random.randint(1 , 6)
    dice2 = random.randint(1 , 6)
    return dice1 , dice2

def pair_dice(dice1 , dice2 , player_name):
    if dice1 == dice2:
        global double_dice_counter
        if double_dice_counter == 2:
            gotojail(player_name)
            return False
        else:
            global double_dice
            double_dice = True
            return True
    return True

def move_to(player_name , step):
    if players[player_name]["position"] + step > 39: #get round reward
        players[player_name]["cash"] += 200
    players[player_name]["position"] = (players[player_name]["position"] + step) % 40
    print(players[player_name]["position"])
    tile_check(player_name , step)
    
def pay(debtor , creditor , value , status): #status can be mandatory or optional
    if players[debtor]["cash"] >= value:
        players[debtor]["cash"] -= value
        players[creditor]["cash"] += value
        return True
    else:
        if status == "optional":
            print("you don't have enough money to pay")
            return False
        
        while players[debtor]["cash"] < value:
            print(f"You are ${value - players[debtor]["cash"]} short.")
            if sell_property(debtor) == False:
                players[creditor]["cash"] += players[debtor]["cash"]
                players[debtor]["cash"] = 0
                players[creditor]["broke"] = True


def sell_property(player_name):
    if players[player_name]["property"] == {}:
        return False
    print(players[player_name]["property"])
    chosen_option = int(input("enter the position of property you want to sell:\n"))
    players[player_name]["property"].pop(chosen_option)
    players[player_name]["cash"] += (tile_information[chosen_option]["buy_price"] // 2)
    tiles[chosen_option]["owner"] = "bank"
            

def tile_check(player_name , step): #define tile's type and related function
    pos = players[player_name]["position"]
    if tiles[pos]["type"] == "street":
        street(player_name , pos)
    elif tiles[pos]["type"] == "community_chest":
        community_chest(player_name , pos)
    elif tiles[pos]["type"] == "tax":
        tax(player_name , pos)
    elif tiles[pos]["type"] == "train":
        train(player_name , pos)
    elif tiles[pos]["type"] == "chance":
        chance(player_name , pos)
    elif tiles[pos]["type"] == "elctric/water":
        electric_water(player_name , pos , step)
    elif tiles[pos]["type"] == "gotojail":
        gotojail(player_name)
    else:
        pass

def street(player_name , pos):
    if tiles[pos]["owner"] == "bank":
        chosen_option = input("enter\n\t1.to buy\n\t2.to pass\n")
        if chosen_option == "1":
            if pay(player_name , "bank" , tile_information[pos]["buy_price"] , "optional") == True:
                tiles[pos]["owner"] = player_name
                players[player_name]["property"][pos] = 0
    
    elif tiles[pos]["owner"] != player_name:
        pay(player_name , tiles[pos]["owner"] , tile_information[pos][ players[ tiles[pos]["owner"] ]["property"][pos] ] , "mandatory")

    else:
        print(f"You own this street: {pos}.{tile_information[pos]["name"]} | color: {tile_information[pos]["color"]} | stage: {players[player_name]["property"][pos]}")
        if build_house_check(player_name , pos) == True and players[player_name]["property"][pos] != 5:
            chosen_option = input("enter\n\t1.to build a house\n\t2.to pass")
            if chosen_option == "1":
                if pay(player_name , "bank" , tile_information[pos]["house_price"] , "optional") == True:
                    players[player_name]["property"][pos] += 1
        

def build_house_check(player_name , pos):
    color_owners = [tiles[i]["owner"] for i in color_index(tile_information[pos]["color"])]
    if (color_owners.count(player_name) == len(color_owners)
        and players[player_name]["property"][pos] == min([players[player_name]["property"][i] for i in color_owners]) ): 
        # if player owns all of the color and the stage of position is minimum
        return True
    else:
        return False


def color_index(color):
    return [x for x in tile_information if tiles[x]["type"] == "street" and tile_information[x].get("color" , False) == color]

def community_chest(player_name , pos):
    pass

def tax(player_name , pos): #tax tiles
    if pos == 4:
        pay(player_name , "bank" , 200 , "mandatory")
    elif pos == 38:
        pay(player_name , "bank" , 100 , "mandatory")

def train(player_name , pos): #train stations
    if tiles[pos]["owner"] != "bank" and tiles[pos]["owner"] != player_name:
        pay(player_name , tiles[pos]["owner"] , 25 * (2 ** (train_own_count(tiles[pos]["owner"]) - 1)) , "mandatory")
    elif tiles[pos]["owner"] == "bank":
        chosen_option = int(input("enter\n\t1.to buy\n\t2.to pass\n"))
        if chosen_option == "1":
            if pay(player_name , "bank" , 200 , "optional") == True:
                tiles[pos]["owner"] = player_name
                players[player_name]["property"][pos] = None
        

def train_own_count(owner): #count how many stations owner got
    owners = [tiles[i]["owner"] for i in [5 , 15 , 25 , 35]]
    return owners.count(owner)

def chance(player_name , pos):
    pass


def electric_water(player_name , pos , step): #electric company and water works
    if tiles[pos]["owner"] != "bank" and tiles[pos]["owner"] != player_name:
        if tiles[pos]["owner"] == tiles[switch_electric_water(pos)]["owner"]:
            pay(player_name , tiles[pos]["owner"] , 10 * step , "mandatory")
        else:
            pay(player_name , tiles[pos]["owner"] , 4 * step , "mandatory")   
    elif tiles[pos]["owner"] == "bank":
        chosen_option = int(input("enter\n\t1.to buy\n\t2.to pass\n"))
        if chosen_option == "1":
            if pay(player_name , "bank" , 150 , "optional") == True:
                tiles[pos]["owner"] = player_name
                players[player_name]["property"][pos] = None
        

def switch_electric_water(pos): #switches between electric company and water works
    if pos == 12: #electric company position
        return 28
    elif pos == 28: #water works position
        return 12

def gotojail(player_name): #go to jail tile
    players[player_name]["jail"] = True
    players[player_name]["position"] = 10 # jail position