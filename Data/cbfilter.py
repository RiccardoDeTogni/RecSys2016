#IMPORT
import time
import numpy as np
import csv
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
		
def extract_tag(items):
	tagv = []
	for item in items:
		tags = item[10].split(',')
		for tag in tags:
			if tag not in tagv:
				tagv.append(tag)
	return tagv
	
tags = extract_tag(items)
print(str(tags))
	

def convertItem(item):
    newItem = []
    newItem.append(intify(item[0]))
    newItem.append(item[1].split(","))
    newItem.append(intify(item[2]))
    newItem.append(intify(item[3]))
    newItem.append(intify(item[4]))
    if item[5] == 'de':
        newItem.append(1)
		newItem.append(0)
		newItem.append(0)
		newItem.append(0)
    elif item[5] == 'at':
		newItem.append(0)
        newItem.append(1)
		newItem.append(0)
		newItem.append(0)
    elif item[5] == 'ch':
		newItem.append(0)
		newItem.append(0)
        newItem.append(1)
		newItem.append(0)
    elif item[5] == 'non_dach':
        newItem.append(0)
		newItem.append(0)
		newItem.append(0)
		newItem.append(1)
    else:
        newItem.append(0)
		newItem.append(0)
		newItem.append(0)
		newItem.append(0)
    newItem.append(intify(item[6]))
    newItem.append(floatify(item[7]))
    newItem.append(floatify(item[8]))
    newItem.append(intify(item[9]))
    newItem.append(item[10].split(","))
    newItem.append(intify(item[11]))
    newItem.append(intify(item[12]))
    return newItem

#Reshape array, convert to int
for i in range(0,len(items)):
    items[i] = convertItem(items[i])


