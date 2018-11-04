# Initialize graph of cities as adjacency matrix

graphofcities = [[0, 2, 2, 5, 7],
                 [2, 0, 4, 1, 2],
                 [2, 4, 0, 1, 3],
                 [5, 1, 1, 0, 2],
                 [7, 2, 3, 2, 0]]
                 # Optimum tour: 0-1-4-3-2-0 cost: 9

# initialize pheromone levels per path
n_cities = len(graphofcities[0])

tau = [ [0, 0.000001, 0.000001, 0.000001, 0.000001], 
		[0.000001, 0.0, 0.000001, 0.000001, 0.000001], 
        [0.000001, 0.000001, 0.0, 0.000001, 0.000001],
        [0.000001, 0.000001, 0.000001, 0.0, 0.000001],
        [0.000001, 0.000001, 0.000001, 0.000001, 0.0] ]

ants = [ [] for i in range(n_cities) ]

def selnextbestcity(i, tabulist,tau, alpha = 1 , beta = 5):
	'''
	Jlist is list of all permissible cities to visit
	'i' is current city
	'tau' is list of lists containing pheromone levels for every edge
	'tabulist' list of cities visited and NOT to visit again
	alpha and beta are constants
	returns probability for one ant and one edge
	'''

	Jlist = set(range(n_cities)).difference(tabulist)   # list of cities where visit is possible
	#print ("Permissible Cities list",Jlist)
	# calculate denominator
	A = [ ((tau[i][j])**alpha) for j in Jlist]
	B = [ ( (1/graphofcities[i][j])**beta) for j in Jlist]

	denominator = sum( [ (i*j) for i,j in zip(A,B)]  )

	cityprob = []

	for j in Jlist:
		numerator = (tau[i][j]**alpha) * ((1/graphofcities[i][j])**beta)
		probability = numerator/denominator
		cityprob.append((j,probability))

	#print ("City Prob list:",cityprob)

	nextcity =  max (cityprob, key = lambda x: x[1] )[0]
	#print ("Next City Chosen:",nextcity)
	return nextcity



def updatepheromonetrail(taumatrix, antpath,rho = 0.5, Q=100, b=5):
	'''
	rho - pheromone evaporation factor
	Q - user defined constant
	antpath - list of lists
	'''
	
	# calculate deltatauk for every ant
	L = []
	for path in antpath:
		L.append( Q / sum( [graphofcities[i][j] for i,j in zip( path, path[1:])] ) )

	deltatau = sum(L)  # addition of all deltataus for ants is final delta tau

	tauij = (1-rho) * taumatrix[i][j] + deltatau

	return tauij



def displayants():
	for i in range(len(ants)):
		print ("Ant:",i,"...Path:",ants[i],"with cost:",calcTourCost(ants[i]))



def calcTourCost(toursequence):
	tourcost = 0

	for i in range(len(toursequence)-1):
		# print (graphofcities[ toursequence[i] ][ toursequence[i+1] ])
		tourcost = tourcost + graphofcities[ toursequence[i] ][ toursequence[i+1] ]

	tourcost = tourcost + graphofcities[ toursequence[-1] ][ toursequence[0] ]  # to complete the cycle
	return tourcost

def disptaumatrix(taumatrix):
	n_cities = len(taumatrix)

	taumatrix = list( map( lambda x: map(lambda y: round(y,2), x)  , taumatrix) )
	
	print ("Pheromone Deposition for respective paths")

	[print ("     {",i,"}",end="") for i in range(n_cities)]

	print ("\n")
	for i in range(len(taumatrix)):	
		print ("{",i,"}", end = " ")
		[print (j, end = "       ") for j in taumatrix[i]]
		print ("\n")
	
