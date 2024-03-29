#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on November 19th 2020

@author: pierre berthet
"""


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from copy import deepcopy




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

	def get_daily_prod_diams(self):
		return self.hired * self.prod * 24 * 2 / 3000

	def get_daily_btc_diams(self):
		return self.hired * self.prod * 24 / 3000



class v1_bot(robot):
	def __init__(self):
		super().__init__(75, 100)


class v2_bot(robot):
	def __init__(self):
		super().__init__(825, 1000)

class v3_bot(robot):
	def __init__(self):
		super().__init__(4500, 5000)

class v4_bot(robot):
	def __init__(self):
		super().__init__(76500, 75000)

class v5_bot(robot):
	def __init__(self):
		super().__init__(229500, 200000)

class v6_bot(robot):
	def __init__(self):
		super().__init__(688500, 500000)



class factory:
	def __init__(self):
		pass

	def get_number_each(self):
		for b in bots:
			print(f"    {b.hired}")



def dpd(prod):
	''' returns diamonds per day, going to production and going to the wallet, prod [electricity per hour]'''
	return 24 * prod *2 / 3000, 24 * prod / 3000



def hours_to(prod, diams=100):
	''' returns number of hours need to produce specified amount of diamonds. prod [electricity per hour]'''
	return diams / (2 * prod / 3000)



def draw_bonus():
	''' return a random int between 10 and 90. Similar to the bonus function giving out diamonds every 20 hours'''
	return np.random.randint(10, 100)


def get_bots_level(bots):
	current_level = 0
	for b, bot in enumerate(bots):
		if bot.hired > 0:
			current_level = b
	if current_level == 0 and bots[current_level].hired == 0:
		print('no bots hired yet?')
	return current_level


def display_bots(bots):
	for i, b in enumerate(bots):
		print(f"    V{i + 1} = {b.hired}")


def get_waiting_days(bots, wallet_prod_balance):
	''' computes the number of days before having accumulated enough diamonds with the current set up to buy a level up bots'''
	current_level = get_bots_level(bots)
	next_level = current_level + 1
	count = 0
	if current_level == 5:
		next_level = current_level
	while wallet_prod_balance < bots[next_level].price: 
		wallet_prod_balance += sum([b.get_daily_prod_diams() for b in bots[:next_level]]) + draw_bonus()
		count += 1

	return count


def get_quickest_level_up_robot_v1(bots, wallet_prod_balance, average=100):
	''' bots: list of the bots
		wallet_prod_balance: int of the current available diamonds for buying robots
		average: int number of simulation run to compute the mean number of days before leveling up (because random in draw_bonus())

		return: min number of days before leveling up, strategy'''		
	current_level = get_bots_level(bots)
	# if current_level == 5:	
	# 	next_level = current_level
	res = []
	local_bots = deepcopy(bots)
	for poss_hire in range((wallet_prod_balance // bots[current_level].price) + 1):
		# print(poss_hire)
		if poss_hire > 0:
			local_bots[current_level].hire_one()
			wallet_prod_balance -= local_bots[current_level].price
		# display_bots(local_bots)
		for d in range(average):
			res.append({'hired': poss_hire, 'wait': get_waiting_days(local_bots, wallet_prod_balance), 'run':d})
	df = pd.DataFrame(res)

	return np.min([df[df.hired == h].wait.mean() for h in df.hired.unique()]), np.argmin([df[df.hired == h].wait.mean() for h in df.hired.unique()])


def get_quickest_level_up_robot_v2(bots, wallet_prod_balance, average=100):
	''' bots: list of the bots
		wallet_prod_balance: int of the current available diamonds for buying robots
		average: int number of simulation run to compute the mean number of days before leveling up (because random in draw_bonus())

		return: min number of days before leveling up, strategy'''		
	current_level = get_bots_level(bots)
	next_level = current_level + 1
	if current_level == 5:
		next_level = current_level
	res = []
	local_bots = deepcopy(bots)
	strat = 0
	min_days = 0
	if (bots[next_level].price / sum([bot.get_daily_prod_diams() for bot in bots]) > bots[current_level].price / bots[current_level].get_daily_prod_diams()) and wallet_prod_balance > bots[current_level].price:
		# min_days = bots[current_level].price / bots[current_level].get_daily_prod_diams()
		strat = 1
	
	min_days = (bots[next_level].price - wallet_prod_balance) / sum([bot.get_daily_prod_diams() for bot in bots])
		
	return min_days, strat


def get_quickest_level_up_robot_v2b(bots, wallet_prod_balance, average=100):
	''' bots: list of the bots
		wallet_prod_balance: int of the current available diamonds for buying robots
		average: int number of simulation run to compute the mean number of days before leveling up (because random in draw_bonus())

		return: min number of days before leveling up, strategy'''		
	current_level = get_bots_level(bots)
	next_level = current_level + 1
	if current_level == 5:
		next_level = current_level
	res = []
	local_bots = deepcopy(bots)
	strat = 0
	min_days = 0
	if ((bots[next_level].price - wallet_prod_balance) / sum([bot.get_daily_prod_diams() for bot in bots]) > bots[current_level].price / bots[current_level].get_daily_prod_diams()) and wallet_prod_balance > bots[current_level].price:
		# min_days = bots[current_level].price / bots[current_level].get_daily_prod_diams()
		strat = 1
	
	min_days = (bots[next_level].price - wallet_prod_balance) / sum([bot.get_daily_prod_diams() for bot in bots])
		
	return min_days, strat



def get_quickest_level_up_robot_v3(bots, wallet_prod_balance, average=100):
	''' bots: list of the bots
		wallet_prod_balance: int of the current available diamonds for buying robots
		average: int number of simulation run to compute the mean number of days before leveling up (because random in draw_bonus())

		return: min number of days before leveling up, strategy'''		
	current_level = get_bots_level(bots)
	next_level = current_level + 1
	if current_level == 5:
		next_level = current_level
	res = []
	local_bots = deepcopy(bots)
	strat = 0
	min_days = 0
	if ((bots[next_level].price - wallet_prod_balance) / sum([bot.get_daily_prod_diams() for bot in bots]) >
		((bots[next_level].price - (wallet_prod_balance - bots[current_level].price )) / (sum([bot.get_daily_prod_diams() for bot in bots]) + bots[current_level].get_daily_prod_diams()))) and wallet_prod_balance > bots[current_level].price:
		# min_days = bots[current_level].price / bots[current_level].get_daily_prod_diams()
		strat = 1
	
	min_days = (bots[next_level].price - wallet_prod_balance) / sum([bot.get_daily_prod_diams() for bot in bots])
		
	return min_days, strat


def get_quickest_level_up_robot_v4(bots, wallet_prod_balance, average=100, max_delay=10):
	''' bots: list of the bots
		wallet_prod_balance: int of the current available diamonds for buying robots
		average: int number of simulation run to compute the mean number of days before leveling up (because random in draw_bonus())

		return: min number of days before leveling up in order to improve BTC prod, strategy'''		
	current_level = get_bots_level(bots)
	next_level = current_level + 1
	if current_level == 5:
		next_level = current_level
	res = []
	local_bots = deepcopy(bots)
	strat = 0
	min_days = 0
	if ((bots[next_level].price - wallet_prod_balance) / sum([bot.get_daily_prod_diams() for bot in bots]) > max_delay) and wallet_prod_balance > bots[current_level].price:
		# min_days = bots[current_level].price / bots[current_level].get_daily_prod_diams()
		strat = 1
	
	min_days = (bots[next_level].price - wallet_prod_balance) / sum([bot.get_daily_prod_diams() for bot in bots])
		
	return min_days, strat

#def __init__():
v1 = v1_bot()
v1.set_hired(10)

v2 = v2_bot()
v3 = v3_bot()
v4 = v4_bot()
v5 = v5_bot()
v6 = v6_bot()


dpd(v1.eph())

# init bots

#bots = [v1, v2]

bots = [v1, v2, v3, v4, v5, v6]

tactics = [get_quickest_level_up_robot_v1, get_quickest_level_up_robot_v2, get_quickest_level_up_robot_v2b, get_quickest_level_up_robot_v3, get_quickest_level_up_robot_v4]
tactics_names = ['strategy 1', 'strategy 2', 'strategy 2b', 'strategy 3', 'Strategy 4']

# init trackers
total_prod = 0


wallet_prod = 490
wallet_btc = 2363

tracker = []

simulate = True

if simulate:
	for tester in range(14):
		wallet_prod = 3000
		wallet_btc = 18000
		v1.set_hired(10)
		v2.set_hired(43)
		v3.set_hired(33)
		v4.set_hired(1)
		v5.set_hired(0)
		v6.set_hired(0)
		notif = True
		verbose = False
		threshold = 1000
		for day in range(1, 365):
			bonus = draw_bonus()
			total_prod += sum([bot.get_daily_prod_diams() for bot in bots])
			wallet_btc += sum([bot.get_daily_btc_diams() for bot in bots])
			wallet_prod += sum([bot.get_daily_prod_diams() for bot in bots]) + bonus

			min_days, strat = get_quickest_level_up_robot_v4(bots, int(wallet_prod), max_delay=tester)
			if verbose:
				print(f"Day {day}: strat is to hire {strat} bots of level {get_bots_level(bots) + 1}, level up bot expected in {min_days}")
			current_level = get_bots_level(bots)

			if strat != 0:
				for hire in range(strat):
					bots[current_level].hire_one()
					wallet_prod -= bots[current_level].price
					print(f"day {day}: +1 V{current_level + 1} bot")
			if get_bots_level(bots) < 5:
				if wallet_prod >= bots[current_level + 1].price:
					bots[current_level + 1].hire_one()
					wallet_prod -= bots[current_level + 1].price
					print(f"day {day}: +1 V{current_level + 2} bot")

			if wallet_btc > threshold and notif:
				print(f"{threshold / (10**6)} btc balance reached, at day {day}")
				threshold = threshold * 2

			tracker.append({'day': day, 'bonus': bonus, 'balance_prod': wallet_prod, 'balance_btc': wallet_btc, 'delay':tester,
							'daily_prod': sum([bot.get_daily_prod_diams() for bot in bots]),
							'daily_wallet_diam': sum([bot.get_daily_btc_diams() for bot in bots])})
		
		print(f'\n\n########## SUMMARY {day + 1} days ##########\n')
		print(f"DELAY MAX = {tester}\n")
		print("B0TS:")
		display_bots(bots)
		print('')
		print(f"FINAL BALANCE: \n    wallet BTC = {np.round(wallet_btc / (10**6), 3)}\n    wallet prod = {int(wallet_prod)}")

	tracker = pd.DataFrame(tracker)
	tracker.plot()
	plt.show()



multi_sim = True
if multi_sim:

	tactics = [get_quickest_level_up_robot_v1, get_quickest_level_up_robot_v2, get_quickest_level_up_robot_v2b, get_quickest_level_up_robot_v3, get_quickest_level_up_robot_v4]
	tactics_names = ['strategy 1', 'strategy 2', 'strategy 2b', 'strategy 3', 'Strategy 4']
	tracker = []


	for sx, strategy in enumerate(tactics):
		total_prod = 0
		wallet_prod = 3000
		wallet_btc = 18000
		v1.set_hired(10)
		v2.set_hired(43)
		v3.set_hired(33)
		v4.set_hired(1)
		v5.set_hired(0)
		v6.set_hired(0)
		notif = True
		verbose = False
		threshold = 1000
		for day in range(1, 600):
			bonus = draw_bonus()
			total_prod += sum([bot.get_daily_prod_diams() for bot in bots])
			wallet_btc += sum([bot.get_daily_btc_diams() for bot in bots])
			wallet_prod += sum([bot.get_daily_prod_diams() for bot in bots]) + bonus

			min_days, strat = strategy(bots, int(wallet_prod))
			if verbose:
				print(f"Day {day}: strat is to hire {strat} bots of level {get_bots_level(bots) + 1}, level up bot expected in {min_days}")
			current_level = get_bots_level(bots)

			if strat != 0:
				for hire in range(strat):
					if wallet_prod >= bots[current_level].price:  # redundant as checked in the strat call but better be safe.
						bots[current_level].hire_one()
						wallet_prod -= bots[current_level].price
						print(f"day {day}: +1 V{current_level + 1} bot")
			if get_bots_level(bots) < 5:
				if wallet_prod >= bots[current_level + 1].price:
					bots[current_level + 1].hire_one()
					wallet_prod -= bots[current_level + 1].price
					print(f"day {day}: +1 V{current_level + 2} bot")

			if wallet_btc > threshold and notif:
				print(f"{threshold / (10**6)} btc balance reached, at day {day}")
				threshold = threshold * 2

			tracker.append({'strategy': tactics_names[sx], 'day': day, 'bonus': bonus, 'balance_prod': wallet_prod, 'balance_btc': wallet_btc,
							'daily_prod': sum([bot.get_daily_prod_diams() for bot in bots]),
							'daily_wallet_diam': sum([bot.get_daily_btc_diams() for bot in bots])})
		display_bots(bots)

	tracker = pd.DataFrame(tracker)
	tracker.plot()
	plt.show()

	sns.lineplot(data=tracker, x='day', y='balance_btc', hue='strategy', alpha=.4)

	plt.show()


'''
Focus on the btv wallet accrual, not on the prod numbers!!!
'''