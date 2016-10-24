

#open files

def similar(item1,item2):
	num = len(item1 & item2)
	den = len(item1) + len (item2)
	res = num/den
	return res
	

def similarset(item, itemz):
	for x in itemz:
		similarity = similar (item,x)
		
	return res
	
	
def ucb(users, users):
	#content-based on users similarity, TO IMPLEMENT
	#save top-pop string
	return res
	
	
def cf(rated, itemz):
	for item in rated:
		similarset = similarset(item, itemz)
		

#file write intestation 

for user in users:
	if not rated:
		suggestions = ucb(user, users)
	else:
		suggestions = cf(rated, itemz)
	
	#file write suggestions

	#output file close