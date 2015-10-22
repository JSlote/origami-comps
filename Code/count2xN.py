""" Program to generate all 2xN flat foldable maps for a given N

In general, assume left-most horizontal crease is a valley

Real answer = final answer * 2

Implementation details:
- each "face" is a tuple (column, row) (a.k.a (x,y)) whose entries are INTS (start @ (1,1))
- graph will be a dictionary whose values are faces, dict[f] is a list of faces adjacent to f
"""

from Queue import Queue
import itertools
import sys
import time

directions = ["N", "S", "E", "W"]
creases = ["M", "V"]

#given one wing of the butterfly, returns the other
def findPair(face, direction):
	# import pdb; pdb.set_trace()
	if direction == "N":
		# if odd then look up, if even look down
		return ( face[0] , face[1]-1 if face[1]%2 else face[1]+1 )
	if direction == "S":
		return ( face[0] , face[1]+1 if face[1]%2 else face[1]-1 )
	elif direction == "E":
		return ( face[0]+1 if face[0]%2 else face[0]-1 , face[1] )
	elif direction == "W":
		return ( face[0]-1 if face[0]%2 else face[0]+1 , face[1] )

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

# determine if there is a path from f to g
def isTherePathFromFtoG(f, g, graph):
	
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


# tests whether this linear ordering satisfies the butterfly condition
# assumes the linear ordering has no faces ommitted or doubled
def satisfiesButterflyCondition(linearOrdering):
	return checkAlong("S", linearOrdering) \
	   and checkAlong("E", linearOrdering) \
	   and checkAlong("W", linearOrdering)

#check butterflies along a particular direction
def checkButterfliesAlong(direction, linOrder):
	def check(incompleteLinOrder):
		if len(incompleteLinOrder) == 0:
			return True

		pair = findPair(incompleteLinOrder[0], direction)

		try:
			pairLoc = incompleteLinOrder.index(pair)
		except ValueError: # no can do
			return False

		return check(incompleteLinOrder[1:pairLoc-1]) and check(incompleteLinOrder[pairLoc+1:])

	# import pdb; pdb.set_trace()
	# for this direction, remove those faces that don't have pairs
	dirLinOrder = [];
	for face in linOrder:
		if findPair(face, direction) in linOrder:
			dirLinOrder.append(face)

	return check(dirLinOrder)

def bruteForceButterflyCheck(linOrder):

	# each butterfly is a tuple (face1, face2)
	# no north butterflies in 2 x n
	sButterflies = []
	wButterflies = []
	eButterflies = []
	N = int(len(linOrder)/2)

	# get the south butterflies (every vertical pair of faces)
	for col in range(1, N):
		if (col,1) in linOrder and (col,2) in linOrder:
			sButterflies.append(((col,1), (col,2)))


	for col in range(1, N, 2):
		if (col,1) in linOrder and (col + 1,1) in linOrder:
			eButterflies.append(((col,1), (col + 1,1)))
		if (col,2) in linOrder and (col + 1,2) in linOrder:
			eButterflies.append(((col,2), (col + 1,2)))

	for col in range(2, N, 2):
		if (col,1) in linOrder and (col - 1,1) in linOrder:
			eButterflies.append(((col,1), (col - 1,1)))
		if (col,2) in linOrder and (col - 1,2) in linOrder:
			eButterflies.append(((col,2), (col - 1,2)))

	noProblemYet = True
	for butterflies in [eButterflies, wButterflies, sButterflies]:
		
		for i in range(len(butterflies)):
			for j in range(i + 1, len(butterflies)):

				b1f1 = linOrder.index(butterflies[i][0])
				b1f2 = linOrder.index(butterflies[i][1])

				b2f1 = linOrder.index(butterflies[j][0])
				b2f2 = linOrder.index(butterflies[j][1])

				
				noProblemYet = noProblemYet and not (b1f1 < b2f1 < b1f2 < b2f2)
				noProblemYet = noProblemYet and not (b1f1 < b2f2 < b1f2 < b2f1)

				noProblemYet = noProblemYet and not (b1f2 < b2f1 < b1f1 < b2f2)
				noProblemYet = noProblemYet and not (b1f2 < b2f2 < b1f1 < b2f1)

				noProblemYet = noProblemYet and not (b2f1 < b1f1 < b2f2 < b1f2)
				noProblemYet = noProblemYet and not (b2f1 < b1f2 < b2f2 < b1f1)

				noProblemYet = noProblemYet and not (b2f2 < b1f1 < b2f1 < b1f2)
				noProblemYet = noProblemYet and not (b2f2 < b1f2 < b2f1 < b1f1)

				if not noProblemYet:
					return False

	return noProblemYet

# test if this incomplete order satisfies the butterfly conditions
def isIncompleteLinearOrderConsistentWithButterfly(incompleteLinearOrder, newestFace):
	
	for direction in ["S","E","W"]:
		if findPair(newestFace, direction) in incompleteLinearOrder:
			if not checkButterfliesAlong(direction, incompleteLinearOrder):
				return False
	return True #bruteForceButterflyCheck(incompleteLinearOrder)

# tests if the incomplete linear order obeys the partial order given by the graph
# only tests the newest face
def isIncompleteLinearOrderConsistentWithGraph(incompleteLinearOrder, newestFace, graph):
	for face in incompleteLinearOrder:
		if incompleteLinearOrder.index(face) > incompleteLinearOrder.index(newestFace):
			if isTherePathFromFtoG(face, newestFace, graph):
				return False
		elif incompleteLinearOrder.index(face) < incompleteLinearOrder.index(newestFace):
			if isTherePathFromFtoG(newestFace, face, graph):
				return False

	return True

# recursively compute whether or not this incomplete linear order is completable
def isIncompleteLinearOrderSatisfiable(incompleteLinearOrder, unorderedFaces, newestFace, graph):

	# if this incomplete linear ordering is not satisfiable, adding more terms won't fix it. so we're done
	if not (isIncompleteLinearOrderConsistentWithButterfly(incompleteLinearOrder, newestFace) and \
	    	isIncompleteLinearOrderConsistentWithGraph(incompleteLinearOrder, newestFace, graph)):
	   return False
	
	# base case: full linear ordering	
	if len(unorderedFaces) == 0:
		return True

	# maybe get this face in a smarter way?
	face = unorderedFaces.pop()
	# add face to every possible location
	for i in range(len(incompleteLinearOrder) + 1):
		newIncompleteLinearOrder = incompleteLinearOrder[:i] + [face] + incompleteLinearOrder[i:]
		result = isIncompleteLinearOrderSatisfiable(newIncompleteLinearOrder, unorderedFaces, face, graph)
		if result:
			return result

# determine if a crease patter is foldable
def isPatternValid(pattern):
	graph = generateGraphFromCreasePattern(pattern)

	unorderedFaces = list(graph.keys())
	face = unorderedFaces.pop()
	incompleteLinearOrder = [face]

	return isIncompleteLinearOrderSatisfiable(incompleteLinearOrder, unorderedFaces, face, graph)

def main():

	try:
		N = int(sys.argv[1]) - 1
	except IndexError, e:
		N = 6-1

	
	listOfPatterns = generateAllCreasePatterns(N)
	
	validPatterns = []
	invalidPatterns = []

	for pattern in listOfPatterns:

		if isPatternValid(pattern):
			validPatterns.append(pattern)
		else:
			invalidPatterns.append(pattern)

	#f = open("outfile" + str(N) + ".txt", "w")
	f = sys.stdout

	f.write("valid: " + str(validPatterns) + "\n")
	f.write("invalid: " + str(invalidPatterns) + "\n")

	f.write("valid: " + str(len(validPatterns)) + "\n")
	f.write("invalid: " + str(len(invalidPatterns)) + "\n")


main()