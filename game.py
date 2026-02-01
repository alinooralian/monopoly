import tkinter as tk
from tkinter import messagebox
import random

players = {
    'player1': {'position':0, 'cash':1500, 'property':{}, 'jail':False, 'dice_counter':3, 'get_out_of_jail_card':False},
    'player2': {'position':0, 'cash':1500, 'property':{}, 'jail':False, 'dice_counter':3, 'get_out_of_jail_card':False},
    'player3': {'position':0, 'cash':1500, 'property':{}, 'jail':False, 'dice_counter':3, 'get_out_of_jail_card':False},
    'player4': {'position':0, 'cash':1500, 'property':{}, 'jail':False, 'dice_counter':3, 'get_out_of_jail_card':False},
    'bank': {'cash':float('inf')}
}
player_list = [p for p in players if p != 'bank']
current_player_index = 0

tiles = {  
    0: {'type':'go','owner':'bank'}, 1:{'type':'street','owner':'bank'}, 2:{'type':'community_chest','owner':'bank'},
    3:{'type':'street','owner':'bank'}, 4:{'type':'tax','owner':'bank'}, 5:{'type':'train','owner':'bank'},
    6:{'type':'street','owner':'bank'}, 7:{'type':'chance','owner':'bank'}, 8:{'type':'street','owner':'bank'},
    9:{'type':'street','owner':'bank'},10:{'type':'jail','owner':'bank'}, 11:{'type':'street','owner':'bank'},
    12:{'type':'utility','owner':'bank'}, 13:{'type':'street','owner':'bank'}, 14:{'type':'street','owner':'bank'},
    15:{'type':'train','owner':'bank'}, 16:{'type':'street','owner':'bank'}, 17:{'type':'community_chest','owner':'bank'},
    18:{'type':'street','owner':'bank'}, 19:{'type':'street','owner':'bank'}, 20:{'type':'free','owner':'bank'},
    21:{'type':'street','owner':'bank'}, 22:{'type':'chance','owner':'bank'}, 23:{'type':'street','owner':'bank'},
    24:{'type':'street','owner':'bank'}, 25:{'type':'train','owner':'bank'}, 26:{'type':'street','owner':'bank'},
    27:{'type':'street','owner':'bank'}, 28:{'type':'utility','owner':'bank'}, 29:{'type':'street','owner':'bank'},
    30:{'type':'gotojail','owner':'bank'},31:{'type':'street','owner':'bank'}, 32:{'type':'street','owner':'bank'},
    33:{'type':'community_chest','owner':'bank'}, 34:{'type':'street','owner':'bank'},35:{'type':'train','owner':'bank'},
    36:{'type':'chance','owner':'bank'}, 37:{'type':'street','owner':'bank'}, 38:{'type':'tax','owner':'bank'}, 39:{'type':'street','owner':'bank'}
}

tile_information = {
    1: {'name':'Mediterranean Avenue','color':'Brown','buy_price':60,'house_price':50,0:2,1:10,2:30,3:90,4:160,5:250},
    3: {'name':'Baltic Avenue','color':'Brown','buy_price':60,'house_price':50,0:4,1:20,2:60,3:180,4:320,5:450},
    6: {'name':'Oriental Avenue','color':'Light Blue','buy_price':100,'house_price':50,0:6,1:30,2:90,3:270,4:400,5:550},
    8: {'name':'Vermont Avenue','color':'Light Blue','buy_price':100,'house_price':50,0:6,1:30,2:90,3:270,4:400,5:550},
    9: {'name':'Connecticut Avenue','color':'Light Blue','buy_price':120,'house_price':50,0:8,1:40,2:100,3:300,4:450,5:600},
    11:{'name':'St. Charles Place','color':'Pink','buy_price':140,'house_price':100,0:10,1:50,2:150,3:450,4:625,5:750},
    13:{'name':'States Avenue','color':'Pink','buy_price':140,'house_price':100,0:10,1:50,2:150,3:450,4:625,5:750},
    14:{'name':'Virginia Avenue','color':'Pink','buy_price':160,'house_price':100,0:12,1:60,2:180,3:500,4:700,5:900}
}

chance_cards = [
    {'text':'Advance to Boardwalk','action':lambda p: advance_to(p,39)},
    {'text':'Go to Jail','action':lambda p: goto_jail(p)},
    {'text':'Collect $50','action':lambda p: pay('bank',p,50,'mandatory')}
]

community_chest_cards = [
    {'text':'Get Out of Jail Free','action':lambda p: give_jail_card(p)},
    {'text':'Collect $100','action':lambda p: pay('bank',p,100,'mandatory')}
]

def roll_dice():
    return random.randint(1,6), random.randint(1,6)

def pay(creditor, debtor, amount, status='mandatory'):
    if players[debtor]['cash'] >= amount:
        players[debtor]['cash'] -= amount
        if creditor != 'bank':
            players[creditor]['cash'] += amount
        messagebox.showinfo('Payment', f'{debtor} paid ${amount} to {creditor}')
        return True
    else:
        if status == 'optional':
            messagebox.showinfo('Payment', f'{debtor} does not have enough money!')
            return False
        while players[debtor]['cash'] < amount:
            if not sell_property(debtor):
                messagebox.showinfo('Bankrupt', f'{debtor} went bankrupt!')
                players['bank']['cash'] += players[debtor]['cash']
                players[debtor]['cash'] = 0
                player_list.remove(debtor)
                return False
        return True

def sell_property(player_name):
    if not players[player_name]['property']:
        return False
    prop = random.choice(list(players[player_name]['property'].keys()))
    price = 50
    players[player_name]['cash'] += price
    tiles[prop]['owner'] = 'bank'
    del players[player_name]['property'][prop]
    return True

def goto_jail(player):
    players[player]['position'] = 10
    players[player]['jail'] = True
    messagebox.showinfo('Jail', f'{player} is sent to Jail!')

def give_jail_card(player):
    players[player]['get_out_of_jail_card'] = True
    messagebox.showinfo('Card', f'{player} received a Get Out of Jail Free card')

def advance_to(player,pos):
    if players[player]['position'] > pos:
        players[player]['cash'] += 200
    players[player]['position'] = pos

def next_turn():
    global current_player_index
    current_player_index = (current_player_index + 1) % len(player_list)
    update_gui()

def update_gui():
    player = player_list[current_player_index]
    current_player_label.config(text=f'Current Player: {player}')
    player_info_text.delete('1.0', tk.END)
    for p in player_list:
        info = f"{p}: Cash=${players[p]['cash']}, Position={players[p]['position']}, Properties={list(players[p]['property'].keys())}\n"
        player_info_text.insert(tk.END, info)

def roll_dice_action():
    player = player_list[current_player_index]
    if players[player]['jail']:
        messagebox.showinfo('Jail', f'{player} is in Jail. Use card or pay to get out.')
        next_turn()
        return
    die1, die2 = roll_dice()
    new_pos = (players[player]['position'] + die1 + die2) % 40
    players[player]['position'] = new_pos
    tile = tiles[new_pos]
    if tile['type'] == 'street' and tile['owner'] == 'bank':
        buy = messagebox.askyesno('Street', f'{player} landed on street. Buy for $100?')
        if buy:
            if pay('bank',player,100,'optional'):
                tile['owner'] = player
                players[player]['property'][new_pos] = 0
    elif tile['type'] == 'street' and tile['owner'] != player:
        pay(tile['owner'], player, 20, 'mandatory')
    if random.random() < 0.2:
        card = random.choice(chance_cards)
        messagebox.showinfo('Chance Card', card['text'])
        card['action'](player)
    if random.random() < 0.2:
        card = random.choice(community_chest_cards)
        messagebox.showinfo('Community Chest', card['text'])
        card['action'](player)
    update_gui()
    next_turn()

def build_house_action():
    player = player_list[current_player_index]
    if players[player]['property']:
        prop = random.choice(list(players[player]['property'].keys()))
        players[player]['property'][prop] += 1
        messagebox.showinfo('Build House', f'{player} built a house on property {prop}')
    else:
        messagebox.showinfo('Build House', f'{player} has no properties.')
    update_gui()
    next_turn()

window = tk.Tk()
window.title('🎲 Monopoly GUI Full 🎲')
window.geometry('500x500')
window.configure(bg='#FFF0F5')

header_font = ('Comic Sans MS',16,'bold')
button_font = ('Comic Sans MS',12,'bold')

current_player_label = tk.Label(window, text='', bg='#FFF0F5', fg='#FF69B4', font=header_font)
current_player_label.pack(pady=10)

player_info_text = tk.Text(window, width=60, height=15, font=('Comic Sans MS',11))
player_info_text.pack(pady=10)

roll_button = tk.Button(window, text='Roll Dice', command=roll_dice_action, width=25, height=2, bg='#FFB6C1', fg='white', font=button_font)
roll_button.pack(pady=5)

build_button = tk.Button(window, text='Build House', command=build_house_action, width=25, height=2, bg='#FFB6C1', fg='white', font=button_font)
build_button.pack(pady=5)

exit_button = tk.Button(window, text='Exit', command=window.destroy, width=25, height=2, bg='#FFB6C1', fg='white', font=button_font)
exit_button.pack(pady=5)

update_gui()
window.mainloop()