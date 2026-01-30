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




