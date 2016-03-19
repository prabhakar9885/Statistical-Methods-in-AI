#!/bin/python

# python driver_Random_Sampling.py <numberOfTrials> <k> <file-1> <feature-count-1> <file-2> <feature-count-2> ...

import math as m
import sys
import kthNearestNeighbour_randomSampling as knc

res = {};
numberOfTrials = int( sys.argv[1] )
fractionForTrainingSet = 0.5
k = int( sys.argv[2] )

# print len(sys.argv)

for fileNum in range( 3, len(sys.argv)-1, 2 ):
	sum = 0
	squareSum = 0;
	filename = sys.argv[fileNum];
	numberOfFeatures = int(sys.argv[fileNum+1]);

	for i in range( numberOfTrials ):
		print "=*="*23
		print "Trial-" + str(i+1) + ": "
		val = knc.doKthNearestNeighbourClassification( filename, numberOfFeatures, fractionForTrainingSet, k )
		sum += val
		squareSum += (sum*sum)
		print "Accuracy: " + str(val*100) + "\n"
	mean = sum*1.0/numberOfTrials;
	res[filename] = ( "Mean: " + str(mean*100), "SD: " + str(m.sqrt(squareSum/numberOfTrials - mean)) )

print "=*="*23
print "Overall Mean and Standard Deviation(SD)"
print res