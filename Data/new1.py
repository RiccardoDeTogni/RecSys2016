#IMPORT
import time
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
    targets = list(reader)[1:]
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
'''	
for item in items:
	item = convertItem(item)
'''
for i in range(0,len(items)):
	items[i] = convertItem(items[i])
#similarity
itemActive = [x for x in items if x[12] == 1]


f = open('ratings.csv','w')
i = 0
for user in targets:
	rated = {}
	ratings = {}
	#extract items that user interacted
	for interaction in interactions:
		if interaction[0] == user[0]:
			rated[intify(interaction[1])] = intify(interaction[2])
	#print rated
	
	#set Top Popular items if user has no interaction
	if not rated:
		f.write(str(user[0]) + ', ' + '2778525 1244196 1386412 657183 2791339\n')
		i += 1
		print('user ' + str(i))
		
	else:
		ratedvec = []
		#extract rated items
		for item in items:
			if intify(item[0]) in rated:
				ratedvec.append(item)
		#print(ratedvec)
		
		#calculate estimated ratings for all items
		for item1 in itemActive:
			num = 0
			#den = []
			j = 0
			#print item1
			for item2 in ratedvec:
				#print('hello there')
				sum = 0
				norma = 0
				normb = 0
				a = item1[1].split(',')
				b = item2[1].split(',')
				for title in a:
					if title in b:
						sum +=1
				norma += len(a)
				normb += len(b)
				if item1[2] == item2[2]:
					sum +=1
				norma += 1
				normb += 1
				if item1[3] == item2[3]:
					sum +=1
				norma += 1
				normb += 1
				if item1[4] == item2[4]:
					sum +=1
				norma += 1
				normb += 1
				if item1[5] == item2[5]:
					sum +=1
				if item1[5] == 1:
					if item1[6] == item2[6]:
						sum +=1
						norma += 1
						normb += 1
				norma += 1
				normb += 1
				if item1[9] == item2[9]:
					sum +=1
				norma += 1
				normb += 1
				a = item1[10].split(',')
				b = item2[10].split(',')
				for tag in a:
					if tag in b:
						sum +=1
				norma += len(a)
				normb += len(b)
				
				#print(str(intify(rated[item2[0]])*sum/(math.sqrt(norma*normb))) + ' ' + str(rated[item2[0]]) + ' ' + str(sum))
				num += (intify(rated[item2[0]])*sum/(math.sqrt(norma*normb)))
				#den.append(sum/(math.sqrt(norma*normb)))
			
			#print (num)
			
			ratings[item1[0]] = num
			#print(ratings[item1[0]])
			#f.write(str(a) + '\n')
			
		i += 1	
		sorted_x = sorted(ratings.items(), key=operator.itemgetter(1), reverse=True)
		#print(sorted_x[1])
		f.write(str(user[0]) + ', ')
		u = 0
		v = 0
		while (u < 5):
			if(sorted_x[v] not in rated):
				#print(sorted_x[v])
				f.write(str(sorted_x[v][0]) + ' ')
				u += 1
				v += 1
			else:
				v += 1
		f.write('\n')
		print('user ' + str(i))

	