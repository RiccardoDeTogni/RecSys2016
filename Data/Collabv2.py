#IMPORT
import datetime
import numpy as np
import csv
import os
import math
import operator
from collections import defaultdict
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial


#LOADING DATASETS
#Loading interactions
#pool = ThreadPool(8)

with open('interactions.csv', 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    interactions = list(reader)[1:]
with open('item_profile.csv', 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    items = list(reader)
    item_headers = items[0]
    items = items[1:]
with open('user_profile.csv', 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    users = list(reader)[1:]
with open('target_users.csv', 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    targets = list(reader)[3750:5000]
with open('item_user_dataset.csv', 'rb') as f:
	reader = csv.reader(f, delimiter=',')
	itemUsersList = list(reader)[0:]
print "Loaded datasets"

def intify(str):
    try:
        return int(str)
    except ValueError, ex:
        return int(-1)

def floatify(str):
    try:
        return float(str)
    except ValueError, ex:
        return float(-1)

def convertItem(item):
    newItem = []
    newItem.append(intify(item[0]))
    newItem.append(item[1])
    newItem.append(intify(item[2]))
    newItem.append(intify(item[3]))
    newItem.append(intify(item[4]))
    if item[5] == 'de':
        newItem.append(1)
    elif item[5] == 'at':
        newItem.append(2)
    elif item[5] == 'ch':
        newItem.append(3)
    elif item[5] == 'non_dach':
        newItem.append(4)
    else:
        newItem.append(0)
    newItem.append(intify(item[6]))
    newItem.append(floatify(item[7]))
    newItem.append(floatify(item[8]))
    newItem.append(intify(item[9]))
    newItem.append(item[10])
    newItem.append(intify(item[11]))
    newItem.append(intify(item[12]))
    return newItem


#build dictionary item : [user that rated it]
def build_ItemUser(itemUsersList):
	itemUsers = defaultdict(set)
	for x in itemUsersList:
		for y in x[1].split(' '):
			itemUsers[intify(x[0])].add(intify(y))
	return itemUsers

#build target set
def build_target(targets):
	target_set = []
	for x in targets:
		target_set.append(intify(x[0]))
	return target_set
#build dictionary user : [rated items]
def build_rated(interactions, target_set):
	rated = defaultdict(list)
	tmp_set = set(target_set)
	for interaction in interactions:
		if(intify(interaction[0]) in tmp_set):
			for i in range (0, intify(interaction[2])):
				rated[intify(interaction[0])].append(intify(interaction[1]))
	return rated

def similar(item1,item2):
	l1 = len(item1)
	l2 = len(item2)
	if l1<=2 and l2<=2:
		res = 0
	else:
		num = len(set.intersection(item1,item2))
		den = math.sqrt(l1*l2) + 3
		res = num/den
	return res

#build set of active items iD
def actives(items):
	active = [intify(x[0]) for x in items if intify(x[12]) == 1]
	return set(active)

'''
def build_similarset(itemID, itemUsers):

	itemratings = defaultdict(list)

	for key in itemUsers:
		similarity = similar(itemUsers[itemID],itemUsers[key])
		itemratings[itemID].append()

	return res
'''

def ucb(user, users):
	#content-based on users similarity, TO IMPLEMENT
	#save top-pop string
	res ='2778525 1244196 1386412 657183 2791339'
	return res


def cf(ratedList, itemUsers):
	ratings = {item : 0 for item in activeItems}
	tmp_set = set(ratedList)
	for item1 in ratedList:
		for key, value in itemUsers.iteritems():
			if key in activeItems and key not in tmp_set:
				ratings[key] += similar(itemUsers[item1], value)
				'''if key == 1443706:
					print similar(itemUsers[item1], value)'''
	sorted_x = sorted(ratings, key=ratings.get, reverse=True)
	return str(' '.join(map(str, sorted_x[:5])))
#file write intestation

#build dictionary user: [rated items]

target_set = build_target(targets)

rated = build_rated(interactions, target_set)

itemUsers = build_ItemUser(itemUsersList)

activeItems = actives(items)

print len(activeItems)
#print activeItems
filename= 'collab' + str(datetime.datetime.utcnow().strftime('%I.%M.%S')) + '.csv'
f = open(filename, 'w')
f.write('user_id,recommended_items\n')
#print 'hi3'
i=3750
for user in target_set:
	#print len(rated[user])
	print 'User ' + str(i)
	if user not in rated:
		suggestions = ucb(user, users)
		#print str(user) + ' '
	else:
		suggestions = cf(rated[user], itemUsers)
		#print 'hi'
	submission = str(user) + ',' + suggestions + '\n'
	f.write(submission)
	i += 1
	#file write suggestions

	#output file close
