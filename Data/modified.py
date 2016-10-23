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
'''		
titlev = []
tagv = []
disciplinesv = []
industriesv = []

if not os.path.isfile('tags.csv') or not os.path.isfile('industries.csv') or not os.path.isfile('titles.csv') or not os.path.isfile('disciplines.csv'):    


	#extract all possible features

	for item in items:
		tags = item[10].split(',')
		for tag in tags:
			if tag not in tagv:
				tagv.append(intify(tag))
		
		disc = intify(item[3])
		if disc not in disciplinesv:
			disciplinesv.append(disc)
			
		industry = intify(item[4])
		if industry not in industriesv:
			industriesv.append(industry)
		
		titles = item[1].split(',')
		for tit in titles:
			if tit not in titlev:
				titlev.append(intify(tit))

	print 'features retrievied...'
	tags = open('tags.csv','w')
	titles = open('titles.csv','w')
	disciplines = open('disciplines.csv','w')
	industries = open('industries.csv','w')

	#caching features
	for tag in tagv:
		tags.write(str(tag) + '\n')
	for title in titlev:
		titles.write(str(title) + '\n')
	for discipline in disciplinesv:
		disciplines.write(str(discipline) + '\n')
	for industry in industriesv:
		industries.write(str(industry) + '\n')
else:
	tags = open('tags.csv','r')
	titles = open('titles.csv','r')
	disciplines = open('disciplines.csv','r')
	industries = open('industries.csv','r')
	
	for line in tags:
		tagv.append(intify(line))
	for line in titles:
		titlev.append(intify(line))
	for line in disciplines:
		disciplinesv.append(intify(line))
	for line in industries:
		industriesv.append(intify(line))
	print 'features retrievied...'
	

tags.close()
titles.close()
disciplines.close()
disciplines.close()
industries.close()	
'''

def convertItem(item):
	newItem = []
	newItem.append(intify(item[0]))
    
	titletemp = item[1].split(",")
	newItem.append(titletemp)
	
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
    
	for i in range(0,17):
		if i == intify(item[6]):
			newItem.append(1)
		else:
			newItem.append(0)
            
	newItem.append(floatify(item[7]))
	newItem.append(floatify(item[8]))
    
	for i in range(0,6):
		if intify(item[9]) == i:
			newItem.append(1)
		else :
			newItem.append(0)
      
    
	tagtemp = item[10].split(',')
	
	newItem.append(tagtemp)
        
	newItem.append(intify(item[11]))
	newItem.append(intify(item[12]))
	
	return newItem

if not os.path.isfile('matrix.csv'):
	matrix = open('matrix.csv','w')
	#Reshape array, convert to int
	i = 0
	for item in items:
		item = convertItem(item)
		
	#ciclo di similarità
	
else:
	matrix = open('matrix.csv','r')



