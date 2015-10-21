""" Program to generate all 2xN flat foldable maps for a given N

In general, assume left-most horizontal crease is a valley

Real answer = final answer * 2

Implementation details:
- each "face" is a tuple (column, row) (a.k.a (x,y)) whose entries are INTS (start @ (1,1))
- graph will be a dictionary whose values are faces, dict[f] is a list of faces adjacent to f

partialButterflySatisfied(partialLinearOrder, newestFace):
	
	for dir in [N,S,W]:
		if newestFace's partner in is partialLinearOrder:
			if not spider function:
				return False

	return True

graphSatisfied(partialLinearOrder, newestFace, graph):
	for each a in partialLinearOrder:
		if a > newestFace:
			make sure path from a to newestFace in graph
		else:
			make sure path from newestFace to a in graph

function(partialLinearOrder, unorderedFaces, newestFace):
	
	if len(unorderedFaces) == 0:
		return True

	if partialButterflySatisfied(partialLinearOrder, newestFace) and graphSatisfied(partialLinearOrder, newestFace, graph):

		pick a face from unorderedFaces
		for way to add face to partialLinearOrder:
			result = function(partialLinearOrderIncludingNewFace, unorderedFacesWithoutNewFace, newestFace)
			if result:
				return result

	return False

"""

from queue import Queue
import itertools
import sys
import time

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

# determine if a crease patter is foldable
def isPatternValid(pattern):
	graph = generateGraphFromCreasePattern(pattern)

	return True

# tests whether this linear ordering satisfies the butterfly condition
# assumes the linear ordering has no faces ommitted or doubled
def satisfiesButterflyCondition(linearOrdering):

	# new version has these requirements:
	# given an arbitrary subset of the total linear ordering, check if it satisfies

	# For each direction:
	# 1. Remove all the faces in the partial lin ordering with no pair also in the linear ordering
	# 2. Recursively parse the tree


	def checkAlong(direction, linOrder):
		N = len(linOrder)/2;

		### IN PROGRESS ###
		# Trim the linear ordering as needed (depending on direction)
		# to remove wings that have no pair
		# if direction == "E" and N%2 == 1:
		# 	linOrder = list(set(linOrder) - set([(1,N),(2,N)]))
		# elif direction == "W" and N%2 == 0:
		# 	linOrder = list(set(linOrder) - set([(1,1),(2,1),(1,N),(2,N)]))
		# elif direction == "W" and N%2 == 1:
		# 	linOrder = list(set(linOrder) - set([(1,1),(2,1)]))

			#  No Bugs Here.
			#
			#     / ,, \ 	
			#  |  \::::/ |
			#   \__(  )__/
			#  ____[  ]____
			# /  // \/ \\  \
			#   / | /\ | \
			#   |  \__/  |
			#    \      /

		#given one wing of the butterfly, returns the other
		def findPair(face, direction):
			# import pdb; pdb.set_trace()
			if direction == "N":
				return ( face[0]+1 if face[0]%2 else face[0]-1, face[1] )
			if direction == "S":
				return ( face[0]+1 if face[0]%2 else face[0]-1, face[1] )
			elif direction == "E":
				return ( face[0] , face[1]+1 if face[1]%2 else face[1]-1)
			elif direction == "W":
				return ( face[0] , face[1]-1 if face[1]%2 else face[1]+1)

		#the recursion
		def check(linOrder):
			#base condition
			if len(linOrder) == 0:
				return True

			pair = findPair(linOrder[0], direction)

			try:
				pairLoc = linOrder.index(pair)
			except ValueError: # no can do
				return False

			return check(linOrder[1:pairLoc-1]) and check(linOrder[pairLoc+1:])

		return check(linOrder)
	
	return checkAlong("S", linearOrdering) \
	   and checkAlong("E", linearOrdering) \
	   and checkAlong("W", linearOrdering)

def main():

	N = int(sys.argv[1]) - 1
	
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

	f.write("valid: " + str(len(validPatterns)) + "\n")
	f.write("invalid: " + str(len(invalidPatterns)) + "\n")

	f.write("valid: " + str(validPatterns) + "\n")
	f.write("invalid: " + str(invalidPatterns) + "\n")

main()