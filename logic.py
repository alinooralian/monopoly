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
