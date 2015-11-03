# upwardsPlanarTesting.py
# Sam Vinitsky
# Goal: try to find a flat foldable crease pattern which does not admit an upward planar embedding

# crease pattern will be stored in a 2d array (col, row)
# assume top-left-most horizontal crease is a valley
# top-left-most face is (0,0)

# n columns, m rows
def generateMxNCreasePatterns(m,n):

	# MxN cp has (m-1 x n-1) vertices
	m = m-1
	n = n-1
	
	directions = ["N","S","W","E"]
	cps = []

	for k in range(4 ** (m + n)):
		
		cp = []

		for i in range(m):
			inner = []
			for j in range(n):
				
				power = m*i + j
				
				remainder = k % 4**(power + 1)
				index = int(remainder / 4**power)
				
				inner.append(directions[index])
			cp.append(inner)

		cps.append(cp)
	
	return cps

# returns the adjacency list (dict) of the graph underlying the cp
def convertCreasePatternToGraph(cp):
	
	m = len(cp)
	n = len(cp[0])

	adjList = {}
	
	# +1 because one more face than vertex in each row/col
	for j in range(m+1):
		for i in range(n+1):			
			adjList[(i,j)] = []

	# one vertex at a time
	for j in range(m):

		if j == 0:
			leftHorizontal = "V"
			leftMostHorizontal = "V"
		else:
			# switch
			if (cp[j-1][0] in ["N","E"] and cp[j][0] in ["N","W"]) or \
			   (cp[j-1][0] in ["S","W"] and cp[j][0] in ["S","E"]):

				if leftMostHorizontal == "V":
					leftHorizontal = "M"
					leftMostHorizontal = "M"
				elif leftMostHorizontal == "M":
					leftHorizontal = "V"
					leftMostHorizontal = "V"
			# keep it
			else:
				leftHorizontal = leftMostHorizontal

		for i in range(n):
			if cp[j][i] == "N":
				if leftHorizontal == "V" and (i+j) % 2 == 0 or \
				   	leftHorizontal == "M" and (i+j) % 2 == 1:

					adjList[(i,j)].append((i,j+1))
					adjList[(i+1,j)].append((i,j))
					adjList[(i+1,j+1)].append((i,j+1))
					adjList[(i+1,j+1)].append((i+1,j))
				# other way around
				else:
					adjList[(i,j+1)].append((i,j))
					adjList[(i,j)].append((i+1,j))
					adjList[(i,j+1)].append((i+1,j+1))
					adjList[(i+1,j)].append((i+1,j+1))
				
			if cp[j][i] == "S":
				if leftHorizontal == "V" and (i+j) % 2 == 0 or \
				   	leftHorizontal == "M" and (i+j) % 2 == 1:

					adjList[(i,j)].append((i,j+1))
					adjList[(i,j)].append((i+1,j))
					adjList[(i,j+1)].append((i+1,j+1))
					adjList[(i+1,j+1)].append((i+1,j))
				# other way around
				else:
					adjList[(i,j+1)].append((i,j))
					adjList[(i+1,j)].append((i,j))
					adjList[(i+1,j+1)].append((i,j+1))
					adjList[(i+1,j)].append((i+1,j+1))
			
			if cp[j][i] == "W":
				if leftHorizontal == "V" and (i+j) % 2 == 0 or \
				   	leftHorizontal == "M" and (i+j) % 2 == 1:

					adjList[(i,j)].append((i,j+1))
					adjList[(i+1,j)].append((i,j))
					adjList[(i+1,j)].append((i+1,j+1))
					adjList[(i,j+1)].append((i+1,j+1))
				# other way around
				else:
					adjList[(i,j+1)].append((i,j))
					adjList[(i,j)].append((i+1,j))
					adjList[(i+1,j+1)].append((i+1,j))
					adjList[(i+1,j+1)].append((i,j+1))

				# switch
				if leftHorizontal == "V":
					leftHorizontal = "M"
				else:
					leftHorizontal = "V"

			if cp[j][i] == "E":
				if leftHorizontal == "V" and (i+j) % 2 == 0 or \
				   	leftHorizontal == "M" and (i+j) % 2 == 1:

					adjList[(i,j)].append((i,j+1))
					adjList[(i,j)].append((i+1,j))
					adjList[(i+1,j)].append((i+1,j+1))
					adjList[(i+1,j+1)].append((i,j+1))
				# other way around
				else:
					adjList[(i,j+1)].append((i,j))
					adjList[(i+1,j)].append((i,j))
					adjList[(i+1,j+1)].append((i+1,j))
					adjList[(i,j+1)].append((i+1,j+1))
				
				# switch
				if leftHorizontal == "V":
					leftHorizontal = "M"
				else:
					leftHorizontal = "V"

	return adjList

def main():
	m = 3
	n = 4

	creasePatterns = generateMxNCreasePatterns(m,n)
	# graphs = []
	# for cp in creasePatterns:
		# graphs.append(convertCreasePatternToGraph(cp))

	cp = [["N","N", "S"], [ "S", "E", "W"]]
	out = convertCreasePatternToGraph(cp)
	for j in range(m):
		for i in range(n):
			print((i,j), out[(i,j)])

if __name__ == "__main__":
	main()


