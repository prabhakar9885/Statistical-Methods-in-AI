#!/usr/bin/python
import sys
from matplotlib import pyplot as ppl
import numpy as np

w1 = [(1, 6), (7, 2), (8, 9), (9, 9), (4, 8), (8, 5)]
w2 = [(2, 1), (3, 3), (2, 4), (7, 1), (1, 3), (5, 2), (8, 4)]

# Adding new data elements
w1.extend( [(4, 6), (1, 8), (5, 5)] )
w2.extend( [(2, 2), (4, 2), (6, 1), (2, 4.3)] )

w1_x = [ i[0] for i in w1 ]
w1_y = [ i[1] for i in w1 ] 
w2_x = [ i[0] for i in w2 ]
w2_y = [ i[1] for i in w2 ]

augmented_Tain_set = [ np.array( [[1], [i[0]], [i[1]]] ) for i in w1 ]
augmented_Tain_set.extend( [ np.array( [[-1], [-i[0]], [-i[1]]] ) for i in w2 ] )

axes = ppl.gca()
axes.set_xlim( [0, max(max(w1_x),max(w2_x)) +1] )
axes.set_ylim( [0, max(max(w1_y),max(w2_y))+1] )

ppl.plot( w1_x, w1_y, "bo", label="w1" )
ppl.plot( w2_x, w2_y, "ro", label="w2" )

count = 0

def getWeightsForPerceptron( b, perceptronType ):
	wt_vector = np.array( [[230+count], [-57.5], [-78.3]] )  # Column Vector
	iteration=0
	i=0
	while i<len(augmented_Tain_set):
		y = wt_vector.transpose().dot( augmented_Tain_set[i] )
		if perceptronType=="Widro-Hoff LMS":
			etha = 0.01
			wt_vector += etha * ( b - wt_vector.transpose().dot(augmented_Tain_set[i]) ) * augmented_Tain_set[i];
			i+=1;
	return wt_vector;


"""
Widro-Hoff LMS
"""
import time
while count< 10000:
	st_time = time.time()
	wt_vector = getWeightsForPerceptron( 1, "Widro-Hoff LMS" );
	ppl.plot( [-float(wt_vector[0][0])/float(wt_vector[1][0]), 0], 
			  [0, -float(wt_vector[0][0]) / float(wt_vector[2][0])], "c-")
	print "Widro-Hoff LMS"
	print "=============="
	print wt_vector;
	print time.time()-st_time, "secs"
	print " "
	count+=50


ppl.legend()
ppl.show();