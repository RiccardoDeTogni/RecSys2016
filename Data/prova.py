import numpy as np
import collections
csv = np.genfromtxt ('interactions.csv', dtype='int', delimiter='\t', skip_header = 1)

itemz = np.genfromtxt('item_profile.csv', dtype='int', delimiter='\t', skip_header = 1)

userz = np.genfromtxt('target_users.csv', dtype='int', delimiter='\t', skip_header = 1)

second = csv[:,1]

actives = itemz[:,[0,12]]


non_actives = actives[actives[:,1] == 0]

non_actives = non_actives[:,0]
count = collections.Counter()

for item in second:
	count[item] += 1
	

top5gen = count.most_common(5)
top5gen = np.asarray(top5gen)
top5gen = top5gen[:,0]
#print(count.most_common(5))	
#res = [x for x in count and x[0] in actives]

for item in non_actives:
	count[item] = 0
	
print (count.most_common(5))

top5 = count.most_common(5)
top5 = np.asarray(top5)
top5 = top5[:,0]

f = open('toppop_active.csv','w')
f2 = open('toppop.csv','w')
f.write('user_id,recommended_items\n')
f2.write('user_id,recommended_items\n')

for i in userz:
	f.write(str(i) + ',' + str(top5[0])+ ' ' + str(top5[1])+ ' ' + str(top5[2])+ ' ' + str(top5[3])+ ' ' + str(top5[4]) + '\n')
	f2.write(str(i) + ',' + str(top5gen[0])+ ' ' + str(top5gen[1])+ ' ' + str(top5gen[2])+ ' ' + str(top5gen[3])+ ' ' + str(top5gen[4]) + '\n')
	
	#f.write(np.array2string(np.hstack((i,top5))))



