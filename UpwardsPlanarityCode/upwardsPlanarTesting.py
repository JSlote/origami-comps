# upwardsPlanarTesting.py
# Sam Vinitsky
# Goal: try to find a flat foldable crease pattern which does not admit an upward planar embedding

# crease pattern will be stored in a 2d array
# (col, row)

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
				
				inner.append(index)
			cp.append(inner)

		cps.append(cp)
	
	return cps

def main():
	m = 5
	n = 5

	MxNCreasePatterns = generateMxNCreasePatterns(m,n)

if __name__ == "__main__":
	main()


