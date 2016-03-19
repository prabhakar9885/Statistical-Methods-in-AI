"""
	Questions answered:
	===================
	Implement the following algorithms:
		2. Single-sample perceptron
		3. Single-sample perceptron with margin
		4. Relaxation algorithm with margin
		5. Widrow-Hoff or Least Mean Squared (LMS) Rule

	A. In each case, plot the data points in a graph (e.g. Circle: class= 1 and Cross: class= 2 ) and
	   also show the weight vector a learnt from all of the above algorithms in the same graph
	   (labeling clearly to distinguish different solutions).
"""

#!/usr/bin/python
import sys
from matplotlib import pyplot as ppl
import numpy as np

w1 = [(1, 6), (7, 2), (8, 9), (9, 9), (4, 8), (8, 5)]
w2 = [(2, 1), (3, 3), (2, 4), (7, 1), (1, 3), (5, 2)]

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




def getWeightsForPerceptron( b, perceptronType ):
	if perceptronType=="Widro-Hoff LMS":
		wt_vector = np.array( [[230], [-57.5], [-78.3]] )  # Column Vector
	else:
		wt_vector = np.array( [[0.5], [-0.5], [1.5]] )  # Column Vector
	i=0
	iteration=0
	while i<len(augmented_Tain_set):
		y = wt_vector.transpose().dot( augmented_Tain_set[i] )
		if perceptronType=="Widro-Hoff LMS":
			etha = 0.01
			wt_vector += etha * ( b - wt_vector.transpose().dot(augmented_Tain_set[i]) ) * augmented_Tain_set[i];
			i+=1;
		elif y<=b:
			if perceptronType=="Relaxation":
				etha = 2.5
				wt_vector +=  etha * ((float((b - y)) / sum([j[0]*j[0] for j in augmented_Tain_set[i]])) * augmented_Tain_set[i])
			else:
				etha = 0.5
				wt_vector += etha*augmented_Tain_set[i];
			i=0;
		else:
			i+=1;
		iteration+=1
		if iteration > 100000:
			break;
	return wt_vector;


"""
Single Sample Perceptron
"""
if len(sys.argv)!= 2:
	print "Pass the arguments"
	print "SingleSamplePerceptron"
	print "SingleSamplePerceptronWithMargin"
	print "Relaxation"
	print "LMS"


if sys.argv[1] == "SingleSamplePerceptron" or sys.argv[1] == "all":
	wt_vector = getWeightsForPerceptron( 0, "SingleSamplePerceptron" );
	ppl.plot( [-float(wt_vector[0][0]) / float(wt_vector[1][0]), 0], 
				[0, -float(wt_vector[0][0]) / float(wt_vector[2][0])], "b--", label="Zero Margin")
	print "Single Sample Perceptron"
	print "========================"
	print wt_vector;

if sys.argv[1] == "SingleSamplePerceptronWithMargin" or sys.argv[1] == "all":
	"""
	Single Sample Perceptron With Margin
	"""
	wt_vector = getWeightsForPerceptron( 1, "SingleSamplePerceptronWithMargin" );
	ppl.plot( [-float(wt_vector[0][0]) / float(wt_vector[1][0]), 0], 
			  [0, -float(wt_vector[0][0]) / float(wt_vector[2][0])], "r--", label="With Margin")
	print "Single Sample Perceptron With Margin"
	print "===================================="
	print wt_vector;

if sys.argv[1] == "Relaxation" or sys.argv[1] == "all":
	"""
	Single Sample Perceptron With Relaxation procedure
	"""
	wt_vector = getWeightsForPerceptron( 1, "Relaxation" );
	ppl.plot( [-float(wt_vector[0][0])/float(wt_vector[1][0]), 0], 
			  [0, -float(wt_vector[0][0]) / float(wt_vector[2][0])], "g-", label="Relaxation")
	print "Single Sample Perceptron With Relaxation procedure"
	print "=================================================="
	print wt_vector;

if sys.argv[1] == "LMS" or sys.argv[1] == "all":
	"""
	Widro-Hoff LMS
	"""
	wt_vector = getWeightsForPerceptron( 1, "Widro-Hoff LMS" );
	ppl.plot( [-float(wt_vector[0][0])/float(wt_vector[1][0]), 0], 
			  [0, -float(wt_vector[0][0]) / float(wt_vector[2][0])], "c-", label="Widro-Hoff LMS")
	print "Widro-Hoff LMS"
	print "=============="
	print wt_vector;

ppl.legend()

if sys.argv[1] != "all":
	ppl.text(1, max(max(w1_y),max(w2_y)), "Weight Vector" )
	ppl.text(1, max(max(w1_y),max(w2_y))-1.1, wt_vector )
	
# ppl.show();
ppl.savefig('./'+
				str(sys.argv[1])+'.png', bbox_inches='tight')