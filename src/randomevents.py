import random, groupy
from groupy import Bot

def roll(bot, requester, range=7):
    roll = random.randrange(1, range)
    bot.post("{0} rolls the d-{1} and rolls a {2}".format(requester, range-1, roll))

def flip(bot, requester):
    flip = random.randrange(0, 2)
    bot.post("{0} flips and gets {1}".format(requester, ('heads' if flip == 0 else 'tails')))