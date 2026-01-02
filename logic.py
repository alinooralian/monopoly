import random
players = { "player1" : { "position": 0 , "cash": 1500 , "broke": False , "jail": False , "get_out_of_jail_card": False , "dice_counter": 3 , "property": {} } , 
            "player2" : { "position": 0 , "cash": 1500 , "broke": False , "jail": False , "get_out_of_jail_card": False , "dice_counter": 3 , "property": {} } ,
            "player3" : { "position": 0 , "cash": 1500 , "broke": False , "jail": False , "get_out_of_jail_card": False , "dice_counter": 3 , "property": {} } ,
            "player4" : { "position": 0 , "cash": 1500 , "broke": False , "jail": False , "get_out_of_jail_card": False , "dice_counter": 3 , "property": {} } ,
            "bank"    : { "cash": float('inf')} }

tiles = { 0  : { "type": ""                , "owner": "bank" } ,
          1  : { "type": "street"          , "owner": "bank" } ,
          2  : { "type": "community_chest" , "owner": "bank" } ,
          3  : { "type": "street"          , "owner": "bank" } ,
          4  : { "type": "tax"             , "owner": "bank" } ,
          5  : { "type": "train"           , "owner": "bank" } ,
          6  : { "type": "street"          , "owner": "bank" } ,
          7  : { "type": "chance"          , "owner": "bank" } ,
          8  : { "type": "street"          , "owner": "bank" } ,
          9  : { "type": "street"          , "owner": "bank" } ,
          10 : { "type": ""                , "owner": "bank" } ,
          11 : { "type": "street"          , "owner": "bank" } ,
          12 : { "type": "elctric/water"   , "owner": "bank" } ,
          13 : { "type": "street"          , "owner": "bank" } ,
          14 : { "type": "street"          , "owner": "bank" } ,
          15 : { "type": "train"           , "owner": "bank" } ,
          16 : { "type": "street"          , "owner": "bank" } ,
          17 : { "type": "community_chest" , "owner": "bank" } ,
          18 : { "type": "street"          , "owner": "bank" } ,
          19 : { "type": "street"          , "owner": "bank" } ,
          20 : { "type": ""                , "owner": "bank" } ,
          21 : { "type": "street"          , "owner": "bank" } ,
          22 : { "type": "chance"          , "owner": "bank" } ,
          23 : { "type": "street"          , "owner": "bank" } ,
          24 : { "type": "street"          , "owner": "bank" } ,
          25 : { "type": "train"           , "owner": "bank" } ,
          26 : { "type": "street"          , "owner": "bank" } ,
          27 : { "type": "street"          , "owner": "bank" } ,
          28 : { "type": "elctric/water"   , "owner": "bank" } ,
          29 : { "type": "street"          , "owner": "bank" } ,
          30 : { "type": "gotojail"        , "owner": "bank" } ,
          31 : { "type": "street"          , "owner": "bank" } ,
          32 : { "type": "street"          , "owner": "bank" } ,
          33 : { "type": "community_chest" , "owner": "bank" } ,
          34 : { "type": "street"          , "owner": "bank" } ,
          35 : { "type": "train"           , "owner": "bank" } ,
          36 : { "type": "chance"          , "owner": "bank" } ,
          37 : { "type": "street"          , "owner": "bank" } ,
          38 : { "type": "tax"             , "owner": "bank" } ,
          39 : { "type": "street"          , "owner": "bank" } }

tile_information = { 1  : { "name": "Mediterranean Avenue"  , "color": "Brown"      , "buy_price": 60  , "house_price": 50  , 0: 2  , 1: 10  , 2: 30  , 3: 90   , 4: 160  , 5: 250  } ,
                     3  : { "name": "Baltic Avenue"         , "color": "Brown"      , "buy_price": 60  , "house_price": 50  , 0: 4  , 1: 20  , 2: 60  , 3: 180  , 4: 320  , 5: 450  } ,
                     6  : { "name": "Oriental Avenue"       , "color": "Light Blue" , "buy_price": 100 , "house_price": 50  , 0: 6  , 1: 30  , 2: 90  , 3: 270  , 4: 400  , 5: 550  } ,
                     8  : { "name": "Vermont Avenue"        , "color": "Light Blue" , "buy_price": 100 , "house_price": 50  , 0: 6  , 1: 30  , 2: 90  , 3: 270  , 4: 400  , 5: 550  } ,
                     9  : { "name": "Connecticut Avenue"    , "color": "Light Blue" , "buy_price": 120 , "house_price": 50  , 0: 8  , 1: 40  , 2: 100 , 3: 300  , 4: 450  , 5: 600  } ,
                     11 : { "name": "St. Charles Place"     , "color": "Pink"       , "buy_price": 140 , "house_price": 100 , 0: 10 , 1: 50  , 2: 150 , 3: 450  , 4: 625  , 5: 750  } ,
                     13 : { "name": "States Avenue"         , "color": "Pink"       , "buy_price": 140 , "house_price": 100 , 0: 10 , 1: 50  , 2: 150 , 3: 450  , 4: 625  , 5: 750  } ,
                     14 : { "name": "Virginia Avenue"       , "color": "Pink"       , "buy_price": 160 , "house_price": 100 , 0: 12 , 1: 60  , 2: 180 , 3: 500  , 4: 700  , 5: 900  } ,
                     16 : { "name": "St. James Place"       , "color": "Orange"     , "buy_price": 180 , "house_price": 100 , 0: 14 , 1: 70  , 2: 200 , 3: 550  , 4: 750  , 5: 950  } ,
                     18 : { "name": "Tennessee Avenue"      , "color": "Orange"     , "buy_price": 180 , "house_price": 100 , 0: 14 , 1: 70  , 2: 200 , 3: 550  , 4: 750  , 5: 950  } ,
                     19 : { "name": "New York Avenue"       , "color": "Orange"     , "buy_price": 200 , "house_price": 100 , 0: 16 , 1: 80  , 2: 220 , 3: 600  , 4: 800  , 5: 1000 } ,
                     21 : { "name": "Kentucky Avenue"       , "color": "Red"        , "buy_price": 220 , "house_price": 150 , 0: 18 , 1: 90  , 2: 250 , 3: 700  , 4: 875  , 5: 1050 } ,
                     23 : { "name": "Indiana Avenue"        , "color": "Red"        , "buy_price": 220 , "house_price": 150 , 0: 18 , 1: 90  , 2: 250 , 3: 700  , 4: 875  , 5: 1050 } ,
                     24 : { "name": "Illinois Avenue"       , "color": "Red"        , "buy_price": 240 , "house_price": 150 , 0: 20 , 1: 100 , 2: 300 , 3: 750  , 4: 925  , 5: 1100 } ,
                     26 : { "name": "Atlantic Avenue"       , "color": "Yellow"     , "buy_price": 260 , "house_price": 150 , 0: 22 , 1: 110 , 2: 330 , 3: 800  , 4: 975  , 5: 1150 } ,
                     27 : { "name": "Ventnor Avenue"        , "color": "Yellow"     , "buy_price": 260 , "house_price": 150 , 0: 22 , 1: 110 , 2: 330 , 3: 800  , 4: 975  , 5: 1150 } ,
                     29 : { "name": "Marvin Gardens"        , "color": "Yellow"     , "buy_price": 280 , "house_price": 150 , 0: 24 , 1: 120 , 2: 360 , 3: 850  , 4: 1025 , 5: 1200 } ,
                     31 : { "name": "Pacific Avenue"        , "color": "Green"      , "buy_price": 300 , "house_price": 200 , 0: 26 , 1: 130 , 2: 390 , 3: 900  , 4: 1100 , 5: 1275 } ,
                     32 : { "name": "North Carolina Avenue" , "color": "Green"      , "buy_price": 300 , "house_price": 200 , 0: 26 , 1: 130 , 2: 390 , 3: 900  , 4: 1100 , 5: 1275 } ,
                     34 : { "name": "Pennsylvania Avenue"   , "color": "Green"      , "buy_price": 320 , "house_price": 200 , 0: 28 , 1: 150 , 2: 450 , 3: 1000 , 4: 1200 , 5: 1400 } ,
                     37 : { "name": "Park Place"            , "color": "Dark Blue"  , "buy_price": 350 , "house_price": 200 , 0: 35 , 1: 175 , 2: 500 , 3: 1100 , 4: 1300 , 5: 1500 } ,
                     39 : { "name": "Boardwalk"             , "color": "Dark Blue"  , "buy_price": 400 , "house_price": 200 , 0: 50 , 1: 200 , 2: 600 , 3: 1400 , 4: 1700 , 5: 2000 } , 
                       
                     5  : { "name": "Reading Railroad"      } ,
                     15 : { "name": "Pennsylvania Railroad" } ,
                     25 : { "name": "B. & O. Railroad"      } ,
                     35 : { "name": "Short Line"            } ,
                       
                     12 : { "name": "Electric Company" } ,
                     28 : { "name": "Water Works"      } ,

                     4  : { "name": "Income Tax" } ,
                     38 : { "name": "Luxury Tax" } }



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