import random

chance_cards = [
    {"text": "Advance to Go"                               , "action": lambda player_name: advance_to(player_name, 0)} ,
    {"text": "Advance to Illinois Avenue"                  , "action": lambda player_name: advance_to(player_name, 24)} ,
    {"text": "Advance to St. Charles Place"                , "action": lambda player_name: advance_to(player_name, 11)} ,
    {"text": "Advance to nearest Utility"                  , "action": lambda player_name: advance_to(player_name, 12)} ,
    {"text": "Advance to nearest Railroad"                 , "action": lambda player_name: advance_to(player_name, 5)} ,
    {"text": "Bank pays you dividend of $50"               , "action": lambda player_name: pay("bank" , player_name , 50 , "mandatory")} ,
    {"text": "Get Out of Jail Free"                        , "action": lambda player_name: give_jail_card(player_name)} ,
    {"text": "Go Back 3 Spaces"                            , "action": lambda player_name: mave_to(player_name , -3)} ,
    {"text": "Go to Jail"                                  , "action": lambda player_name: gotojail(player_name)} ,  
    {"text": "Make general repairs on all your property"   , "action": lambda player_name: pay_per_house(player_name, houses=0, hotels=0)} ,
    {"text": "Pay poor tax of $15"                         , "action": lambda player_name: pay(player_name , "bank" , 15 , "mandatory")} ,
    {"text": "Take a trip to Reading Railroad"             , "action": lambda player_name: advance_to(player_name , 5)} ,
    {"text": "Take a walk on the Boardwalk"                , "action": lambda player_name: advance_to(player_name , 39)} ,
    {"text": "You have been elected Chairman of the Board" , "action": lambda player_name: pay(player_name , "bank" , 50 , "mandatory")} ,
    {"text": "Your building loan matures – Receive $150"   , "action": lambda player_name: pay(player_name , "bank" , 150 , "mandatory")} ,
    {"text": "Advance to nearest Railroad"                 , "action": lambda player_name: advance_to(player_name , 15)} 
]


community_chest_cards = [
    {"text": "Advance to Go"                                               , "action": lambda player_name: advance_to(player_name , 0)} ,
    {"text": "Bank error in your favor – Collect $200"                     , "action": lambda player_name: pay("bank" , player_name , 200 , "mandatory")} ,
    {"text": "Doctor’s fee – Pay $50"                                      , "action": lambda player_name: pay(player_name, "bank" , 50 , "mandatory")} ,
    {"text": "From sale of stock you get $50"                              , "action": lambda player_name: pay("bank" , player_name , 50 , "mandatory")} ,
    {"text": "Get Out of Jail Free"                                        , "action": lambda player_name: give_jail_card(player_name)} ,
    {"text": "Go to Jail"                                                  , "action": lambda player_name: gotojail(player_name)} ,
    {"text": "Holiday fund matures – Receive $100"                         , "action": lambda player_name: pay("bank" , player_name , 100 , "mandatory")} ,
    {"text": "Income tax refund – Collect $20"                             , "action": lambda player_name: pay("bank" , player_name , 20 , "mandatory")} ,
    {"text": "It is your birthday – Collect $10"                           , "action": lambda player_name: pay("bank" , player_name , 10 , "mandatory")} ,
    {"text": "Life insurance matures – Collect $100"                       , "action": lambda player_name: pay("bank" , player_name , 100 , "mandatory")} ,
    {"text": "Pay hospital fees of $100"                                   , "action": lambda player_name: pay(player_name , "bank" , 100 , "mandatory")} ,
    {"text": "Pay school fees of $150"                                     , "action": lambda player_name: pay(player_name , "bank" , 150 , "mandatory")} ,
    {"text": "Receive $25 consultancy fee"                                 , "action": lambda player_name: pay("bank" , player_name , 25 , "mandatory")} ,
    {"text": "You are assessed for street repairs"                         , "action": lambda player_name: pay_per_house(player_name, houses=0, hotels=0)} ,
    {"text": "You have won second prize in a beauty contest – Collect $10" , "action": lambda player_name: pay("bank" , player_name , 10 , "mandatory")} ,
    {"text": "You inherit $100"                                            , "action": lambda player_name: pay("bank" , player_name , 100 , "mandatory")}
]

def advance_to(player_name , pos):
    players[player_name]["position"] = pos
    
def give_jail_card(player_name):
    players[player_name]["get_out_of_jail_card"] = True

def pay_per_house(player_name, houses, hotels, house_cost=25, hotel_cost=100):
    cost = houses * house_cost + hotels * hotel_cost
    pay(player_name , "bank" , cost , "mandatory")




def chance_card_coming(player_name):
    card = random.choice(chance_cards)
    print("🎲 Chance:", card["text"])
    card["action"](player_name)

def community_card_coming(player_name):
    card = random.choice(community_chest_cards)
    print("📦 Community Chest:", card["text"])
    card["action"](player_name)