import acoback as ACO
import random as rm
max_it = 10

# initialize pheromone trail

n_ants = len( ACO.graphofcities[1] )
n_cities = len( ACO.graphofcities[1] )
iterLbest = 1000  # best tour cost
tourbest = []  # best tour found
finaltourbest = []
finaltourcost = 1000
Q = 100
rho = 0.5
b = 5
taumatrix = ACO.tau

print ("Number of Cities:",n_cities)
print ("Number of Ants:",n_ants)


for t in range(max_it):   # for maximum number of iterations
	
	# initialize ants to random nodes
	for k in ACO.ants:
		k.clear()         # clear path for every ant
		k.append( rm.randint(0, n_cities-1) ) # choose a random start point city

	# STEP 1. Build Tour For every ant
	for k in ACO.ants:
		i = k[-1]

		# compute (n_cities-1) times, to build a tour
		# Build entire tours from initialized cities	
		for temp in range(n_cities-1):
			k.append( ACO.selnextbestcity(i, k, taumatrix, alpha = 1 , beta = 5) )

	# STEP 2. Find Best Tour found by any ant
	maxtuple = min( [ (k,ACO.calcTourCost(k) ) for k in ACO.ants], key = lambda x: x[1] )
	itertourbest, iterLbest = maxtuple[0], maxtuple[1]

	print ("\n********** In iteration",t,"************")
	ACO.displayants()
	print ("--Best Tour found:",itertourbest,"with cost:",iterLbest,"--")

	if (iterLbest < finaltourcost):
		finaltourbest, finaltourcost = itertourbest, iterLbest

	assert (finaltourcost <= iterLbest),(iterLbest,finaltourcost)

	deltataubest = Q/iterLbest

	# STEP 3. UPDATE Pheromone
	for k in ACO.ants:  # choose k th ant

		c = ACO.calcTourCost(k)
		for i in range(n_cities-1):  # for all adjacent pair combinations in ants
			taumatrix[ k[i] ][ k[i+1] ] =  (1-rho) * taumatrix[ k[i] ][ k[i+1] ] + (Q/c)
			taumatrix[ k[i+1] ][ k[i] ] =  (1-rho) * taumatrix[ k[i+1] ][ k[i] ] + (Q/c)

			# search for tuple in best tour
			t1 = list( zip(tourbest,tourbest[1:]) ).__contains__( (k[i],k[i+1]) )
			t2 = list( zip(tourbest,tourbest[1:]) ).__contains__( (k[i+1],k[i]) )
			if (t1 and t2): # search for edge tuple in best path
				taumatrix[ k[i] ][ k[i+1] ] =+ (b * deltataubest)
				taumatrix[ k[i+1] ][ k[i] ] =+ (b * deltataubest)
			else:
				continue
	print ("\n\nTau Matrix after",t,"iteration:\n")
	ACO.disptaumatrix(taumatrix)
print ("\nBest tour after",max_it,"iterations:",finaltourbest,"with cost:",finaltourcost)
