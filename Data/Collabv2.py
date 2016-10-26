#IMPORT
import datetime
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
    targets = list(reader)[7:10]
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

#TODO convert_user
def convert_user(user):
	newUser = []
	newUser.append(intify(user[0]))
	newUser.append(user[1])
	newUser.append(intify(user[2]))
	newUser.append(intify(user[3]))
	newUser.append(intify(user[4]))
	if user[5] == 'de':
		newUser.append(1)
	elif user[5] == 'at':
		newUser.append(2)
	elif user[5] == 'ch':
		newUser.append(3)
	elif user[5] == 'non_dach':
		newUser.append(4)
	else:
		newUser.append(0)
	newUser.append(intify(user[6]))
	newUser.append(intify(user[7]))
	newUser.append(intify(user[8]))
	newUser.append(intify(user[9]))
	newUser.append(intify(user[10]))
	newUser.append(user[11])
	return newUser

def compare(i1,i2):
	if isinstance(i1, int) or isinstance(i1, float):
		if i1 == i2:
			return 1
		else:
			return 0
	else:
		i2 = i2.split(",")
		i1 = i1.split(",")

		den = math.sqrt(len(i1)*len(i2)) + 2
		counter = 0
		for i in range(len(i1)):
			for j in range(len(i2)):
				if i1[i] == i2[j]:
					counter +=1
		return counter / float(den)

def fennecSim(i1,i2):
	score = 0
	weights = [0,1.8,0.3,0.85,0.3,0.7,0,0,0.6,1.5,0,0] #magic numbers
	for i in range(1,min(len(i2),len(i1))):
		#print i1[i], i2[i]
		score += compare(i1[i],i2[i]) #* weights[i]
	return score

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

#build testset
def build_user(users):
	user_set = []
	for x in users:
		user_set.append(intify(x[0]))
	return user_set
#build test dict userID: [user]
def build_user_dict(users):
	user_dict = defaultdict(list)
	for x in users:
		user_dict[intify(x[0])] = convert_user(x)
	return user_dict
#build dictionary user : [rated items]
def build_rated(interactions, target_set):
	rated = defaultdict(list)
	tmp_set = set(target_set)
	for interaction in interactions:
		if(intify(interaction[0]) in tmp_set):
			rated[intify(interaction[0])].append(intify(interaction[1]))
	return rated

def build_explicit_rated(interactions, target_set):
	rated_ex = defaultdict(list)
	tmp_set = set(target_set)
	for interaction in interactions:
		if(intify(interaction[0]) in tmp_set):
			rated_ex[intify(interaction[0])].append(list(intify(interaction[1]), intify(interaction[2])))
	return rated_ex

#TODO similarity user-user through attributes
def similarUserUser(user1, user2):
	res = 0
	return res

#item-item similarity
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

#find n nearest neighbours of a user
def find_neighbours(userID, n):
	compare = defaultdict(list)
	neighbours = defaultdict(list)
	tmp_set = set(user_set)
	for user in tmp_set:
		if user != userID:
			#print user_dict[userID]
			compare[user] = fennecSim(user_dict[userID], user_dict[user])
	sorted_compare = sorted(compare.items(), key=operator.itemgetter(1), reverse=True)
	for i in range (0, n):
		neighbours[userID].append(sorted_compare[i])
	#print neighbours
	return neighbours


def toppop():
	#content-based on users similarity, TO IMPLEMENT
	#save top-pop string
	res ='2778525 1244196 1386412 657183 2791339'
	return res

def contentUserUser(user):
    ratings = {item : 0 for item in activeItems}
    similar_users = find_neighbours(user, 200)
    #print user_dict[user]
    for key, value in similar_users.iteritems():
	#print str(key) + ' ' + str(value)
        for item in set(rated[value[0]]):
            ratings[item] += value[1]
    sorted_x = sorted(ratings, key=ratings.get, reverse=True)
    return str(' '.join(map(str, sorted_x[:5])))

def cf(ratedList, itemUsers):
	ratings = {item : 0 for item in activeItems}
	tmp_set = set(ratedList)
	for item1 in ratedList:
		for key, value in itemUsers.iteritems():
			if key in activeItems and key not in tmp_set:
				ratings[key] += similar(itemUsers[item1], value)
	sorted_x = sorted(ratings, key=ratings.get, reverse=True)
	return str(' '.join(map(str, sorted_x[:5])))
#file write intestation

#build dictionary user: [rated items]

target_set = build_target(targets)

user_set = build_user(users)

user_dict = build_user_dict(users)
#print user_dict
rated = build_rated(interactions, target_set)

itemUsers = build_ItemUser(itemUsersList)

activeItems = actives(items)

#print len(activeItems)
#print activeItems
filename= 'hybrid' + str(datetime.datetime.utcnow().strftime('%I.%M.%S')) + '.csv'
f = open(filename, 'w')
f.write('user_id,recommended_items\n')
#print 'hi3'
i=1
for user in target_set:
	#print len(rated[user])
	print 'User ' + str(i)
	if user not in rated:
		suggestions = contentUserUser(user)
		#print str(user) + ' '
	else:
		suggestions = cf(rated[user], itemUsers)
		#print 'hi'
	submission = str(user) + ',' + suggestions + '\n'
	f.write(submission)
	i += 1
	#file write suggestions

	#output file close
