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
            
