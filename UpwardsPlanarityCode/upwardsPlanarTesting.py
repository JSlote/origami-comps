# upwardsPlanarTesting.py
# Sam Vinitsky
# Goal: try to find a flat foldable crease pattern which does not admit an upward planar embedding

# crease pattern will be stored in a 2d array (row, col)
# assume top-left-most horizontal crease is a valley
# 0 is mountain, 1 is valley
# top-left-most face is (0,0)

# follows Joe's counting argument
# O(2^(mn)) 
def generateSeededCP(m, n, topAssignmentDec, leftAssignmentDec, verticesAssignmentDec):

	# m x n-1
	# verticalCreases[0] is the first ROW of vertical creases
	verticalCreases = []
	# n x m-1
	# horizontalCreases[0] is the first COLUMN of horizontal creases
	horizontalCreases = [] 

	for i in range(m):
		inner = []
		for j in range(n-1):
			inner.append(0)
		verticalCreases.append(inner)

	for i in range(n):
		inner = []
		for j in range(m-1):
			inner.append(0)
		horizontalCreases.append(inner)

	# assign the top-most verts and left-most horzs
	topAssignment = str(bin(topAssignmentDec))[2:]
	leftAssignment = str(bin(leftAssignmentDec))[2:]

	while len(topAssignment) < n-1:
		topAssignment = "0" + topAssignment
	while len(leftAssignment) < m-1:
		leftAssignment = "0" + leftAssignment

	for i in range(len(topAssignment)):
		verticalCreases[0][i] = int(topAssignment[i])

	for i in range(len(leftAssignment)):
		horizontalCreases[0][i] = int(leftAssignment[i])

	# make all the decisions at vertices
	verticesAssignment = str(bin(verticesAssignmentDec))[2:]
	while len(verticesAssignment) < (m-1)*(n-1):
		verticesAssignment = "0" + verticesAssignment

	# where in verticesAssignment we look for our nest decision
	index = 0

	# diagonal we are on (there are m+n-3)
	for diag in range()

	cp = (verticalCreases, horizontalCreases)

	return cp

def generateMxNCreasePatterns(m,n):

	cps = []

	for topAssignmentDec in range(2**(n-1)):
		for leftAssignmentDec in range(2**(m-1)):
			for verticesAssignmentDec in range(2**((m-1)*(n-1))):
				cp = generateSeededCP(m, n, topAssignmentDec, leftAssignmentDec, verticesAssignmentDec)
				# if cp not in cps:
				cps.append(cp)

	return cps

def main():
	m = 5
	n = 4

	creasePatterns = generateMxNCreasePatterns(m,n)
	# for cp in creasePatterns:
	# 	print(cp[0][0] , cp[1][0])

if __name__ == "__main__":
	main()


