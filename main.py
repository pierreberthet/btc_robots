#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on November 19th 2020

@author: pierre berthet
"""


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


class robot:
	
	def __init__(self, prod, price):
		self.prod = prod
		self.price = price
		self.hired = 0
	
	def set_hired(self, hired):
		self.hired = hired

	def hire_one(self):
		self.hired += 1

	def eph(self):
		return self.hired * self.prod


class v1_bot(robot):
	def __init__(self):
		super().__init__(75, 100)


class v2_bot(robot):
	def __init__(self):
		super().__init__(850, 1000)




def dpd(prod):
	''' returns diamonds per day, going to production and going to the wallet, prod [electricity per hour]'''
	return 24 * prod *2 / 3000, 24 * prod / 3000



def hours_to(prod, diams=100):
	''' returns number of hours need to produce specified amount of diamonds. prod [electricity per hour]'''
	return diams / (2 * prod / 3000)



def draw_bonus():
	''' return a random int between 10 and 90. Similar to the bonus function giving out diamonds every 20 hours'''
	return np.random.randint(10, 90)





#def __init__():
v1 = v1_bot()
v1.set_hired(10)

v2 = v2_bot()
#v1.set_hired(10)
# v3 = v3_bot()
# v4 = v4_bot()
# v5 = v5_bot()
# v6 = v6_bot()


dpd(v1.eph())


# init bots

bots = [v1, v2]

# bots = [v1, v2, v3, v4, v5, v6]

# init trackers
total_prod = 0

wallet_btc = 58
wallet_prod = 358


tracker = []

# run day step simulations
for day in range(1, 100):
	bonus = draw_bonus()
	total_prod += sum([dpd(bot.eph())[0] for bot in bots])
	wallet_btc += sum([dpd(bot.eph())[1] for bot in bots])
	wallet_prod += sum([dpd(bot.eph())[0] for bot in bots]) + bonus
	
	if wallet_prod >= v2.price :
		wallet_prod -= v2.price
		v2.hire_one()
	tracker.append({'day': day, 'bonus': bonus, 'balance_prod': wallet_prod, 
					'daily_prod': sum([dpd(bot.eph())[0] for bot in bots]),
					'daily_wallet_diam': sum([dpd(bot.eph())[1] for bot in bots])})
	# buy shit based on decisions
	# diam_prod_balance =  


tracker = pd.DataFrame(tracker)
tracker.plot()
plt.show()