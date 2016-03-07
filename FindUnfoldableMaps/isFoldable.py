# isFoldable.py
# determine flat foldability of maps
# Author: Sam Vinitsky
# Date: 3/5/16

# class to store an N by N map
class Map:

	m = 1
	n = 1
	cp = [[]]

	def __init__(self, cp):
		self.cp = cp
		self.m = len(cp) + 1
		self.n = len(cp[0]) + 1 # m x n map is specified by (m-1)x(n-1) creases

	# determine if this linear ordering satisfies the butterfly condition for this map
	def satisfiesButterflyCondition(self, linearOrdering):
		return True

	# determine if this linear ordering satisfies the partial ordering induces by the checkerboard pattern + cp
	def satisfiesPartialOrdering(self, linearOrdering):
		return True

	# map is an N by N array, linear ordering is stored as a list
	# determine if map can be folded into linearOrdering 
	def isLinearOrderingValid(self, linearOrdering):
		
		if self.satisfiesButterflyCondition(linearOrdering):
			if self.satisfiesPartialOrdering(linearOrdering):
				return True

		return False

# an ordering of the faces (0,0) through (m-1,n-1)
class LinearOrdering:

	m = 1 
	n = 1
	linearOrdering = [(0,0)]

	def __init__(self, m, n, lo):
		self.m = m
		self.n = n
		self.linearOrdering = lo



def main():
	cp = [[]]
	myMap = Map(cp)
	myLinearOrdering = LinearOrdering(1, 1, [(0,0)])

	print(myMap.isLinearOrderingValid(myLinearOrdering))


if __name__ == "__main__":
	main()