""" Program to generate all 2xN flat foldable maps for a given N

In general, assume top-left-most vertical crease is a valley

Real answer = final answer * 2

Implementation details:
- each "face" is a tuple (x,y) whose entries are INTS
- graph will be a dictionary whose values are faces, dict[f] is a list of faces adjacent to f

0) linearOrderings = []
1) for each node pair u,v in G: 
	if there is NO path from u to v or from v to u:
		add undirected edge (u,v) to G
2) for every source s in G and every sink t in G:
	if there is a hamiltonian path from s to t:
		add the path to linearOrderings
3) for order in linearOrderings:
	if order satisfies the butterfly condition, return True
4) return False

Plan: 
generateGraphFromCreasePattern: Sam
testButterflyCondition: Joe

"""

N = 3
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
	return {}

# tests whether this linear ordering satisfies the butterfly condition
def testButterflyCondition(linearOrdering):
	return True