#IMPORT
import time
import numpy as np
import csv
import os
from collections import defaultdict
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial


#LOADING DATASETS
#Loading interactions
pool = ThreadPool(4)

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
	
for item in items:
	item = convertItem(item)


#similarity

i = 0
similarity = np.empty([len(items),len(items)], dtype=float, order)

for item1 in items:
	j = 0
	for item2 in items:
   
		sum = 0
		norma = 0
		normb = 0
		a = item[1].split(',')
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
      
		a = item[10].split(',')
		b = item2[10].split(',')
		for tag in a:
			if tag in b:
				sum +=1
      
		norma += len(a)
		normb += len(b)
      
		similarity[i,j] = sum/(math.sqrt(norma*normb))
		similarity[j,i] = similarity [i,j]
		j += 1
   i += 1
   print('element ' + str(i))
   
f = open('matrix.csv')
similarity.tofile(f,sep='\t',format='%s')
	
#Reshape array, convert to int
