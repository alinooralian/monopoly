import random

class Player:
    def __init__(self, name):  
        self.name = name
        self.position = 0
        self.pool = 1500
        self.dar_zendan = False
        self.biron_az_zendan_rayegan = 0

    def move_to(self, pos):
        self.position = pos

    def move_steps(self, steps):
        self.position = (self.position + steps) % 40

    def change_money(self, amount):  
        self.pool += amount

    def bro_be_zendan(self):
        self.position = 10
        self.dar_zendan = True


def advance_to(bazikon, position):
    bazikon.move_to(position)

def bro_be_zendan_card(bazikon):
    bazikon.bro_be_zendan()

def pool_bede(bazikon, amount):
    bazikon.change_money(amount)  

def pool_begir(bazikon, amount):
    bazikon.change_money(-amount)

def give_jail_card(bazikon):
    bazikon.biron_az_zendan_rayegan += 1

def pay_per_house(bazikon, houses, hotels, house_cost=25, hotel_cost=100):
    cost = houses * house_cost + hotels * hotel_cost
    pool_begir(bazikon, cost)


chance_cards = [
    {"text": "Advance to Go", "action": lambda p: advance_to(p, 0)},
    {"text": "Advance to Illinois Avenue", "action": lambda p: advance_to(p, 24)},
    {"text": "Advance to St. Charles Place", "action": lambda p: advance_to(p, 11)},
    {"text": "Advance to nearest Utility", "action": lambda p: advance_to(p, 12)},
    {"text": "Advance to nearest Railroad", "action": lambda p: advance_to(p, 5)},
    {"text": "Bank pays you dividend of $50", "action": lambda p: pool_bede(p, 50)},
    {"text": "Get Out of Jail Free", "action": lambda p: give_jail_card(p)},
    {"text": "Go Back 3 Spaces", "action": lambda p: p.move_steps(-3)},
    {"text": "Go to Jail", "action": lambda p: bro_be_zendan_card(p)},  
    {"text": "Make general repairs on all your property",
     "action": lambda p: pay_per_house(p, houses=0, hotels=0)},
    {"text": "Pay poor tax of $15", "action": lambda p: pool_begir(p, 15)},
    {"text": "Take a trip to Reading Railroad", "action": lambda p: advance_to(p, 5)},
    {"text": "Take a walk on the Boardwalk", "action": lambda p: advance_to(p, 39)},
    {"text": "You have been elected Chairman of the Board",
     "action": lambda p: pool_begir(p, 50)},
    {"text": "Your building loan matures – Receive $150",
     "action": lambda p: pool_bede(p, 150)},
    {"text": "Advance to nearest Railroad", "action": lambda p: advance_to(p, 15)},
]


community_chest_cards = [
    {"text": "Advance to Go", "action": lambda p: advance_to(p, 0)},
    {"text": "Bank error in your favor – Collect $200",
     "action": lambda p: pool_bede(p, 200)},
    {"text": "Doctor’s fee – Pay $50",
     "action": lambda p: pool_begir(p, 50)},
    {"text": "From sale of stock you get $50",
     "action": lambda p: pool_bede(p, 50)},
    {"text": "Get Out of Jail Free",
     "action": lambda p: give_jail_card(p)},
    {"text": "Go to Jail",
     "action": lambda p: bro_be_zendan_card(p)},
    {"text": "Holiday fund matures – Receive $100",
     "action": lambda p: pool_bede(p, 100)},
    {"text": "Income tax refund – Collect $20",
     "action": lambda p: pool_bede(p, 20)},
    {"text": "It is your birthday – Collect $10",
     "action": lambda p: pool_bede(p, 10)},
    {"text": "Life insurance matures – Collect $100",
     "action": lambda p: pool_bede(p, 100)},
    {"text": "Pay hospital fees of $100",
     "action": lambda p: pool_begir(p, 100)},
    {"text": "Pay school fees of $150",
     "action": lambda p: pool_begir(p, 150)},
    {"text": "Receive $25 consultancy fee",
     "action": lambda p: pool_bede(p, 25)},
    {"text": "You are assessed for street repairs",
     "action": lambda p: pay_per_house(p, houses=0, hotels=0)},
    {"text": "You have won second prize in a beauty contest – Collect $10",
     "action": lambda p: pool_bede(p, 10)},
    {"text": "You inherit $100",
     "action": lambda p: pool_bede(p, 100)},
]