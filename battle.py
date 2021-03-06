import sys, traceback
from functions import *
import pymongo
from base import *
import simplejson as json
import tornado.web

def checkState(c1,c2):
    winner = False
    if c1.hp() <= 0:
        print 'Game over, the computer has defeated you!'
        sys.exit(0)
    elif c2.hp() <= 0:
        print 'Well done, you\'ve bested the computer(%s) with %s!'%(c2.name.title(),c1.name.title())
        sys.exit(0)
    else:
        pass

def act(c1,c2):
    a = raw_input('What would you like to do (Type h for help)? -->').lower()
    if a == 'h':
        help()
        return 0
    #using an ability
    elif a == 'q' or a == 'w' or a == 'e' or a == 'r':
        if 'on' in c1.moves[a]:
            g = c1.useAbility(a,[c2],toggle=True)
        else:
            g = c1.useAbility(a,[c2])
        if g:
            return 1

    elif a == 'a':
        c1.autoAttack(c2)
        return 1
    #shop
    elif a == 'p':
        shop(c1)
        return 0
    elif a == 's':
        c1.showStats()
        return 0
    elif a == 'c':
        c1.showStats(True)
        return 0
    elif a == 'enemy':
        c2.showStats()
        return 0
    elif a == 'i':
        c1.showItems()
        return 0
    elif a == 'exit' or a == 'quit':
        sys.exit(0)
    else:
        print 'Invalid input'
        return 0

def help():
    print 'Type (Q|W|E|R) to use that ability.\nType A to auto-attack\nType S for status (hp, mana, ad, ap, as, buffs, and cooldowns)\nType Enemy for opponent status\nType C for current status (all stats)\nType I to show inventory\nType P to shop\nType exit to quit\nEverything is type-insensitive'

def shop(c1):
    c = getChamp('items')
    k = c['items']
    #check if items are full
    while True:
        a = buy(c1,k)
        if a == 1:
            break

def buy(c1, k):
    if len(c1.items) >= 6:
        print 'Items are full, choose item to sell:'
        if not sell(c1,k):
            return 0
    s = raw_input('type an item\'s name to buy it, "list" to see all of the item tags, or "sell" to drop an item -->')
    if s == 'list':
        shoplist(k)
        s = raw_input('type an item\'s name to buy it -->').lower()
    elif s == 'sell':
        sell(c1,k)
    if s in k:
        c1.items.append(s)
        c1.doItems()
        print 'purchased',k[s]['name']+'!'
    else:
        print 'item not found, sorry!'

    l = raw_input('Would you like to keep shopping (Y|N)? -->').lower()
    if l == 'yes' or l == 'y':
        return 0
    else:
        return 1

def sell(c1,k):
    c1.showItems()
    r = raw_input('Which item slot do you want to emtpy? -->')
    try:
        c1.items.pop(int(r))
    except:
        print 'List index out of range, you\'ve been booted from the shop for tomfoolery'
        return 1

def shoplist(k):
    l = []
    for item in k:
        l.append(item.encode('utf-8'))
    l.sort()
    print l

def init(p):

    if p == 1:
        while True:
            inp = raw_input('Who do you want to play as? -->').lower()
            if inp == 'akali' or inp == 'ahri' or inp == 'alistar' or inp == 'amumu' or inp == 'anivia' or inp == 'annie' or inp == 'ashe':
                break
    else:
        inp = 'akali'
    c = getChamp(inp)
    if (inp == 'akali'):
        a = Akali(c)
    elif (inp == 'ahri'):
        a = Ahri(c)
    elif (inp == 'alistar'):
        a = Alistar(c)
    elif (inp == 'amumu'):
        a = Amumu(c)
    elif (inp == 'anivia'):
        a = Anivia(c)
    elif (inp == 'annie'):
        a = Annie(c)
    elif (inp == 'ashe'):
        a = Ashe(c)

    return a

## MAIN ##
c1 = init(1)
c2 = init(2)
while True:
    print ''
    print '===Player\'s Turn==='
    while True:
        a = act(c1,c2)
        if a: 
            break
    checkState(c1,c2)
    try:
        c1.tick(c2)
    except:
        c1.tick()
    print '===Enemy\'s Turn==='
    c2.autoAttack(c1)
    c2.tick()
