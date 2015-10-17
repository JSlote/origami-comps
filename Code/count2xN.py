""" Program to generate all 2xN flat foldable maps for a given N

In general, assume left-most horizontal crease is a valley

Real answer = final answer * 2

Implementation details:
- each "face" is a tuple (row, column) whose entries are INTS (start @ (1,1))
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

Plan: 
getPossibleLinearOrderings: Sam
testButterflyCondition: Joe

"""

from queue import Queue

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

# generate hamiltonian paths
def getHamPaths(f,g,graph):
	return [(1,2), (2,3)]

# get all the possible linear orderings
def getPossibleLinearOrderings(graph):
	linOrders = []
	
	# for each pair of source s, sink t, determine all hampaths from s to t
	# adds these paths to linOrders

	return linOrders

# tests whether this linear ordering satisfies the butterfly condition
def testButterflyCondition(linearOrdering):
	return True

def main():

	N = 5
	#listOfPatterns = generateAllCreasePatterns(N)
	listOfPatterns = ["NEW"]

	validPatterns = []
	for pattern in listOfPatterns:
		directedGraph = generateGraphFromCreasePattern(pattern)
		bidirectedGraph = addBidirectedEdges(directedGraph)
		linOrders = getPossibleLinearOrderings(bidirectedGraph)

		for linOrder in linOrders:
			if testButterflyCondition(linOrder):
				if pattern not in validPatterns:
					validPatterns.append(pattern)

	print(validPatterns)

main()