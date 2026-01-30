import random

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

def advance_to(player_name , pos):
    if players[player_name]["position"] > pos:
        players[player_name]["cash"] += 200
    players[player_name]["position"] = pos


def nearest_railroad(player_name):
    station = ((players[player_name]["position"] // 10) * 10) + 5
    players[player_name]["position"] = station
    train(player_name , station , "chance")


def nearest_utility(player_name):
    if players[player_name]["position"] < 20:
        utility = 12
    else:
        utility = 28
    players[player_name]["position"] = utility
    electric_water(player_name , utility , 0 , "chance")


def give_jail_card(player_name):
    players[player_name]["get_out_of_jail_card"] = True


def pay_per_house(player_name , house , hotel):
    cost = 0
    for stage in players[player_name]["property"].values():
        if stage == 5:
            cost += (hotel + (4 * house))
        else:
            cost += (stage * house)
    
    pay(player_name , "bank" , cost , "mandatory")


def pay_each_player(player_name):
    for p in player_list:
        pay(player_name , p , 50 , "mandatory")


def collect_each_player(player_name):
    for p in player_list:
        pay(p , player_name , 10 , "mandatory")




def chance_card_coming(player_name):
    card = random.choice(chance_cards)
    print("🎲 Chance:", card["text"])
    card["action"](player_name)

def community_card_coming(player_name):
    card = random.choice(community_chest_cards)
    print("📦 Community Chest:", card["text"])
    card["action"](player_name)