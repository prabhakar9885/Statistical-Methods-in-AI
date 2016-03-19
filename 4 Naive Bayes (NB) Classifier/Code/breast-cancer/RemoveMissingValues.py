#!/bin/python

import sys
import csv

filename = sys.argv[1]

print filename

with open(filename, 'rb') as csvfile:
	lines = csv.reader(csvfile)
	filteredFile = open( filename+"-filtered", "wb+" )
	missingLinesCount = 0
	lineCount = 0
	for line in lines:
		if "?" in line:
			missingLinesCount += 1
			continue
		else:
			lineCount += 1
			filteredFile.write( ','.join(line) + '\n' )

	filteredFile.close()

	print( "Total number of lines: " + str(lineCount) )
	print( "Number of lines with missing data: " + str(missingLinesCount) )