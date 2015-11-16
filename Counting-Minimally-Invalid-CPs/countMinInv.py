import sys
import json

def main():
	try:
		N = int(sys.argv[1])
	except IndexError, e:
		print "Please tell me which n"
		return

	with open (str(N)+".out","r") as dataFile:
		invalidCPs = json.load(dataFile)[0]["invalid"]


	with open (str(N-1)+".out","r") as dataFile:
		validMinusOneCPs = json.load(dataFile)[0]["valid"]
	
	mininmallyInvalidCPs = []
	nonMinInvalidCPS = []

	for pattern in invalidCPs:
		if pattern[1:] in validMinusOneCPs and pattern[:-1] in validMinusOneCPs:
			mininmallyInvalidCPs.append(str(pattern))
		else:
			nonMinInvalidCPS.append(str(pattern))


	f = open("invalidCPsFor" + str(N) + ".txt", "w")

	f.write("minimally invalid: " + str(mininmallyInvalidCPs) + "\n")
	f.write("non-min invalid: " + str(nonMinInvalidCPS) + "\n")

	print("minimally invalid: " + str(mininmallyInvalidCPs) + "\n")
	print("non-min invalid: " + str(nonMinInvalidCPS) + "\n")

main()