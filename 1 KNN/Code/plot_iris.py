#!/bin/python

x=[]
y=[]
class1=[]
xyc=[]

import csv
import random
import math as m
import sys
with open(sys.argv[1], 'rb') as csvfile:
	lines = csv.reader(csvfile)
	dataset = list(lines)
	for line in dataset:
		x.append( line[1] )
		y.append( line[3] )
		class1.append( line[4] )
		xyc.append( (line[1], line[3], line[4]) )

lowX, heighX = m.floor(float(min(x))), m.ceil(float(max(x)))
lowY, heighY = m.floor(float(min(y))), m.ceil(float(max(y)))

import numpy as np
x_test = np.arange( lowX, heighX+0.2, 0.2 )
y_test = np.arange( lowY, heighY+0.2, 0.2 )
testSet = []

for i in range(len(x_test)):
	x_test[i], y_test[i] = float("{0:.1f}".format( x_test[i] )), float("{0:.1f}".format( y_test[i] ))

for i in x_test:
	for j in y_test:
		testSet.append([i,j])


import kthNearestNeighbour_randomSampling as knn

resultSet = [];
points = {}
for tSet in testSet:
	prediction = knn.getPrediction( knn.getDistancesOfKSimilarSets( zip(x,y,class1), tSet, 1 ) )
	resultSet.append( tSet )
	a,b = float("{0:.1f}".format( tSet[0] )), float("{0:.1f}".format( tSet[1] ))
	if prediction == "Iris-setosa":
		resultSet[-1].extend( ['r'] )
		points[ (a,b) ] = 'r'
		# print (a,b)
	elif prediction == "Iris-versicolor":
		resultSet[-1].extend( ['y'] )
		points[ (a,b) ] = 'y'
		# print (a,b)
	elif prediction == "Iris-virginica":
		resultSet[-1].extend( ['b'] )
		points[ (a,b) ] = 'b'
		# print (a,b)



from matplotlib import pyplot as ppl
import matplotlib.patches as mpatches

############################################################################################################
#	
#	Plot the test-cases
#
# # Plot Red dots from test-cases
# x_test_r = [ i[0] for i in resultSet if  i[-1]=='r' ]
# y_test_r = [ i[1] for i in resultSet if  i[-1]=='r' ]
# ppl.plot( x_test_r, y_test_r, 'r+', label="Iris-setosa" )

# # # Plot Yellow dots from test-cases
# x_test_y = [ i[0] for i in resultSet if  i[-1]=='y' ]
# y_test_y = [ i[1] for i in resultSet if  i[-1]=='y' ]
# ppl.plot( x_test_y, y_test_y, 'yo', label="Iris-versicolor" )

# # # Plot Blue dots from test-cases
# x_test_b = [ i[0] for i in resultSet if  i[-1]=='b' ]
# y_test_b = [ i[1] for i in resultSet if  i[-1]=='b' ]
# ppl.plot( x_test_b, y_test_b, 'b+', label="Iris-virginica" )

# Plot data-set from the file
isa = ppl.plot( [ i[0] for i in xyc if  i[-1]=='Iris-setosa' ], 
			[ i[1] for i in xyc if  i[-1]=='Iris-setosa' ], 'r+', label="Iris-setosa" )
ivr = ppl.plot( [ i[0] for i in xyc if  i[-1]=='Iris-versicolor' ], 
			[ i[1] for i in xyc if  i[-1]=='Iris-versicolor' ], 'yo', label="Iris-versicolor" )
iva = ppl.plot( [ i[0] for i in xyc if  i[-1]=='Iris-virginica' ], 
			[ i[1] for i in xyc if  i[-1]=='Iris-virginica' ], 'b^', label="Iris-virginica" )
ppl.xlabel("Sepal width")
ppl.ylabel("Petal width")
ppl.legend();
############################################################################################################


# Find decision bounday
def get_closest_point( list, point ):
	list.sort( key = lambda p : (p[0]-point[0])**2 + (p[0]-point[0])**2 )
	return list[0]

bound_ry_x = [];
bound_ry_y = [];

print x_test
print y_test
for i in x_test:
	for j in y_test:
		x1, y1 = float("{0:.1f}".format( i )), float("{0:.1f}".format( j ))
		x1_next, y1_next = float("{0:.1f}".format( i+0.2 )), float("{0:.1f}".format( j+0.2 ))
		# print x1, y1
		if x1_next<=heighX and points[ (x1,y1) ] == 'r' and points[ (x1_next,y1) ] != 'r':
			bound_ry_x.append( x1+0.1 )
			bound_ry_y.append( y1 )
		elif y1_next<=heighY and points[ (x1,y1) ] == 'r' and points[ (x1,y1_next) ] != 'r':
			bound_ry_x.append( x1 )
			bound_ry_y.append( y1+0.1 )


bound_yb_x = [];
bound_yb_y = [];
y_test = y_test[::-1]
for i in x_test:
	for j in y_test:
		x1, y1 = float("{0:.1f}".format( i )), float("{0:.1f}".format( j ))
		x1_next, y1_next = float("{0:.1f}".format( i+0.2 )), float("{0:.1f}".format( j-0.2 ))
		if x1_next<=heighX and points[ (x1,y1) ] == 'b' and points[ (x1_next,y1) ] != 'b':
			bound_yb_x.append( x1+0.1 )
			bound_yb_y.append( y1 )
		elif y1_next>=lowY and points[ (x1,y1) ] == 'b' and points[ (x1,y1_next) ] != 'b':
			bound_yb_x.append( x1 )
			bound_yb_y.append( y1-0.1 )


ppl.plot( bound_ry_x, bound_ry_y, "b-");
ppl.plot( bound_yb_x, bound_yb_y, "b-");

ppl.show();