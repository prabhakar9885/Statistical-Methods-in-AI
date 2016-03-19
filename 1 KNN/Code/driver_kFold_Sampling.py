#!/bin/python

# python driver_Random_Sampling.py <k> <file-1> <feature-count-1>

import math as m
import sys
import kthNearestNeighbour_kFold as knc

res = {};
k = int( sys.argv[1] )
numberOfFolds = 5

# print len(sys.argv)

filename = sys.argv[2];
numberOfFeatures = int(sys.argv[3]);

res = knc.doKthNearestNeighbourClassification( filename, numberOfFeatures, numberOfFolds, k )

def getSD(lst):
	total = sum(lst)
	sd = 0
	for i in lst:
		sd += pow( i-total, 2)
	sd /= 1.0*len(lst)

	import math as m
	return m.sqrt(sd)


print "\n================ " 
print "Over all Result: " 
print "================ " 
print "Mean: " +str( sum(res)*1.0/len(res)*100 )
print "Standard deviation: " +str( getSD(res) )