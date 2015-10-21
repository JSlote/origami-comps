""" Program to generate all 2xN flat foldable maps for a given N

In general, assume left-most horizontal crease is a valley

Real answer = final answer * 2

Implementation details:
- each "face" is a tuple (row, column) (a.k.a (y,x)) whose entries are INTS (start @ (1,1))
- graph will be a dictionary whose values are faces, dict[f] is a list of faces adjacent to f

0) linearOrderings = []
1) for each node pair u,v in G: 
	if there is NO path from u to v or from v to u:
		add bidirected edge (u,v) to G
2) for every source s in G and every sink t in G:
	if there is a hamiltonian path from s to t:
		add the path to linearOrderings
3) for order in linearOrderings:
	if order satisfies the butterfly condition, return True
4) return False
"""

from queue import Queue
import itertools

directions = ["N", "S", "E", "W"]
creases = ["M", "V"]


# recursively generate all NSEW orderings possible
def generateAllCreasePatterns(N):
	
	if N == 1:
		return ["N", "S", "E", "W"]

	allCreasePatterns = []
		
	nMinusOneCreasePatterns = generateAllCreasePatterns(N-1)

	for nMinusOneCP in nMinusOneCreasePatterns:
		for direction in directions:

			thisCreasePattern = nMinusOneCP + direction

			allCreasePatterns.append(thisCreasePattern)

	return allCreasePatterns


# generate graph from crease pattern
def generateGraphFromCreasePattern(cp):
	
	graph = {}
	for row in range(1, 3):
		for col in range(1, len(cp) + 2):
			graph[(col,row)] = []

	# MOUNTAIN:	light  --->  dark
	# VALLEY: 	light  <---  dark

	col = 1
	row = 1
	hCrease = "V" # assignment of the crease going into this vertex from the left
	graph[(1, 2)] = [(1, 1)] # always because first horizontal is valley

	# create the graph
	for col in range(2, len(cp) + 2):

		direction = cp[col - 2]

		# figure out the crease pattern
		if hCrease == "V":
			if direction == "W":
				topVertCrease = "M"
				botVertCrease = "M"
				hCrease = "M"
			elif direction == "E":
				topVertCrease = "V"
				botVertCrease = "V"
				hCrease = "M"
			elif direction == "N":
				topVertCrease = "M"
				botVertCrease = "V"
				hCrease = "V"
			elif direction == "S":
				topVertCrease = "V"
				botVertCrease = "M"
				hCrease = "V"
		elif hCrease == "M":
			if direction == "W":
				topVertCrease = "V"
				botVertCrease = "V"
				hCrease = "V"
			elif direction == "E":
				topVertCrease = "M"
				botVertCrease = "M"
				hCrease = "V"
			elif direction == "N":
				topVertCrease = "V"
				botVertCrease = "M"
				hCrease = "M"
			elif direction == "S":
				topVertCrease = "M"
				botVertCrease = "V"
				hCrease = "M"

		# horizontal crease
		if hCrease == "M":
			# light on top
			if col % 2 == 1:
				graph[(col, row)] = graph[(col, row)] + [(col, row+1)]
			# dark on top
			elif col % 2 == 0:
				graph[(col, row+1)] = graph[(col, row+1)] + [(col, row)]
		elif hCrease == "V":
			# light on top
			if col % 2 == 1:
				graph[(col, row+1)] = graph[(col, row+1)] + [(col, row)]
			# dark on top
			elif col % 2 == 0:
				graph[(col, row)] = graph[(col, row)] + [(col, row+1)]

		# top vertical crease
		if topVertCrease == "M":
			# light on top
			if col % 2 == 1:
				graph[(col, row)] = graph[(col, row)] + [(col-1, row)]
			# dark on top
			elif col % 2 == 0:
				graph[(col-1, row)] = graph[(col-1, row)] + [(col, row)]
		elif topVertCrease == "V":
			# light on top
			if col % 2 == 1:
				graph[(col-1, row)] = graph[(col-1, row)] + [(col, row)]
			# dark on top
			elif col % 2 == 0:
				graph[(col, row)] = graph[(col, row)] + [(col-1, row)]

		# bot vertical crease
		if botVertCrease == "M":
			# light on top
			if col % 2 == 1:
				graph[(col-1, row+1)] = graph[(col-1, row+1)] + [(col, row+1)]
			# dark on top
			elif col % 2 == 0:
				graph[(col, row+1)] = graph[(col, row+1)] + [(col-1, row+1)]
		elif botVertCrease == "V":
			# light on top
			if col % 2 == 1:
				graph[(col, row+1)] = graph[(col, row+1)] + [(col-1, row+1)]
			# dark on top
			elif col % 2 == 0:
				graph[(col-1, row+1)] = graph[(col-1, row+1)] + [(col, row+1)]

	return graph

def areNodesConnected(f,g,graph):
	return areDirectedConnected(f,g,graph) or areDirectedConnected(g,f,graph)

def areDirectedConnected(f,g,graph):
	
	q = Queue(len(graph.keys()))
	seen = [f]

	q.put(f)
	
	while not q.empty():
		
		u = q.get()
		for v in graph[u]:
			if v not in seen:
				q.put(v)
				seen.append(v)


	result = False
	if g in seen:
		result = True

	return result

# adds bidirected edges between nodes that are not connected
def addBidirectedEdges(graph):

	newGraph = {}
	for key in graph.keys():
		newGraph[key] = graph[key]

	for f in graph.keys():
		for g in graph.keys():
			if not areNodesConnected(f, g, graph):
				if f not in newGraph[g]:
					newGraph[g] = newGraph[g] + [f]
				if g not in newGraph[f]:
					newGraph[f] = newGraph[f] + [g]

	return newGraph

# get all the possible linear orderings
def getPossibleLinearOrderings(graph):
	perms = itertools.permutations(graph.keys())
	linOrders = []
	for l in perms:
		listL = []
		for item in l:
			listL.append(item)

		linOrders.append(listL)
	return linOrders

# # tests whether this linear ordering satisfies the butterfly condition
# # assumes the linear ordering has no faces ommitted or doubled
# def satisfiesButterflyCondition(linearOrdering):
# 	def checkAlong(direction, linOrder):
# 		N = len(linOrder)/2;

# 		# Trim the linear ordering as needed (depending on direction)
# 		# to remove wings that have no pair
# 		if direction == "E" and N%2 == 1:
# 			linOrder = list(set(linOrder) - set([(1,N),(2,N)]))
# 		elif direction == "W" and N%2 == 0:
# 			linOrder = list(set(linOrder) - set([(1,1),(2,1),(1,N),(2,N)]))
# 		elif direction == "W" and N%2 == 1:
# 			linOrder = list(set(linOrder) - set([(1,1),(2,1)]))

# 			#  No Bugs Here.
# 			#
# 			#     / ,, \ 	
# 			#  |  \::::/ |
# 			#   \__(  )__/
# 			#  ____[  ]____
# 			# /  // \/ \\  \
# 			#   / | /\ | \
# 			#   |  \__/  |
# 			#    \      /

# 		#given one wing of the butterfly, returns the other
# 		def findPair(face, direction):
# 			# import pdb; pdb.set_trace()
# 			if direction == "N":
# 				return ( face[0]+1 if face[0]%2 else face[0]-1, face[1] )
# 			elif direction == "E":
# 				return ( face[0] , face[1]+1 if face[1]%2 else face[1]-1)
# 			elif direction == "W":
# 				return ( face[0] , face[1]-1 if face[1]%2 else face[1]+1)

# 		#the recursion
# 		def check(linOrder):
# 			#b-b-b-base condition
# 			if len(linOrder) == 0:
# 				return True

# 			pair = findPair(linOrder[0], direction)

# 			try:
# 				pairLoc = linOrder.index(pair)
# 			except ValueError:
# 				return False

# 			return check(linOrder[1:pairLoc-1]) and check(linOrder[pairLoc+1:])

# 		return check(linOrder)
	
# 	return checkAlong("N", linearOrdering) \
# 	   and checkAlong("E", linearOrdering) \
# 	   and checkAlong("W", linearOrdering)

def satisfiesButterflyCondition(linOrder):

	# each butterfly is a tuple (face1, face2)
	# no north butterflies in 2 x n
	sButterflies = []
	wButterflies = []
	eButterflies = []
	N = int(len(linOrder)/2)

	# get the south butterflies (every vertical pair of faces)
	for col in range(1, N):
		sButterflies.append(((col,1), (col,2)))


	for col in range(1, N, 2):
		eButterflies.append(((col,1), (col + 1,1)))
		eButterflies.append(((col,2), (col + 1,2)))

	for col in range(1, N, 2):
		wButterflies.append(((col,1), (col + 1,1)))
		wButterflies.append(((col,2), (col + 1,2)))

	noProblemYet = True
	for butterflies in [eButterflies, wButterflies, sButterflies]:
		
		for i in range(len(butterflies)):
			for j in range(i + 1, len(butterflies)):

				b1f1 = linOrder.index(butterflies[i][0])
				b1f2 = linOrder.index(butterflies[i][1])

				b2f1 = linOrder.index(butterflies[j][0])
				b2f2 = linOrder.index(butterflies[j][1])

				
				noProblemYet = noProblemYet and not (b1f1 < b2f1 < b1f2 < b2f2)

				if not noProblemYet:
					return False

	return noProblemYet

def main():

	N = 3
	listOfPatterns = generateAllCreasePatterns(N)
	
	validPatterns = []
	for pattern in listOfPatterns:
		directedGraph = generateGraphFromCreasePattern(pattern)
		bidirectedGraph = addBidirectedEdges(directedGraph)
		linOrders = getPossibleLinearOrderings(bidirectedGraph)

		for linOrder in linOrders:
			if satisfiesButterflyCondition(linOrder):
				if pattern not in validPatterns:
					validPatterns.append(pattern)

	print(validPatterns)

main()