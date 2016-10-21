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

def extract_title(items):
	titlev = []
	for item in items:
		titles = item[1].split(',')
		for tit in titles:
			if tit not in titlev:
				titlev.append(tit)
	return titlev
	
titles = extract_title(items)
        
def extract_tag(items):
	tagv = []
	for item in items:
		tags = item[10].split(',')
		for tag in tags:
			if tag not in tagv:
				tagv.append(tag)
	return tagv
	
tags = extract_tag(items)

def extract_discipline(items):
   disciplinesv = []
   for item in items:
      disc = intify(item[3])
      if disc not in disciplinesv:
            disciplinesv.append(disc)
            
   return disciplinesv
   
disciplines = extract_discipline(items)

def extract_industry(items):
   industriesv = []
   for item in items:
      industry = intify(item[4])
      if industry not in industriesv:
            industriesv.append(industry)
   return industriesv
   
industries = extract_industry(items)

def convertItem(item):
    newItem = []
    newItem.append(intify(item[0]))
    
    titletemp = item[1].split(",")
    for title in titles:
      if title in titletemp:
         newItem.append(1)
      else:
        newItem.append(0)
        
    for i in range[1,7]:
      if i == intify(item[2]):
         newItem.append(1)
      else:
         newItem.append(0)
         
    for disc in disciplines:
      if intify(item[3]) == disc:
         newItem.append(1)
      else: 
         newItem.append(0)
      
    for industry in industries:
      if intify(item[4]) == indusrty:
         newItem.append(1)
      else:
         newItem.append(0)
    
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
    
      for i in range[0,17]:
         if i == intify(item[6])
            newItem.append(1)
         else:
            newItem.append(0)
            
    newItem.append(floatify(item[7]))
    newItem.append(floatify(item[8]))
    
    for i in range[0,6]
      if intify(item[9]) == i
         newItem.append(1)
      else 
         newItem.append(0)
      
    
    tagtemp = item[10].split(',')
    for tag in tags:
      if tag in tagtemp:
        newItem.append(1)
      else:
        newItem.append(0)
        
    newItem.append(intify(item[11]))
    newItem.append(intify(item[12]))
    return newItem

matrix = open('matrix.csv','w')
#Reshape array, convert to int
for i in range(0,len(items)):
    items[i] = convertItem(items[i])
    matrix.write(items[i])



