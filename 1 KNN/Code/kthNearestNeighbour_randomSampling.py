#!/bin/python

featuresList = [];

def loadDatasetRandSampling(filename, numberOfFeatures, fractionForTrainingSet):
	trainingSet=[]
	testSet=[]

	import csv
	import random
	import math as m
	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    lenghtOfTrainingSet = int(m.floor( fractionForTrainingSet * len(dataset) ))
	    random.shuffle( dataset )

	    for i in range(lenghtOfTrainingSet):
	    	trainingSet.append( dataset[i] )
	    	if dataset[i][-1] not in featuresList:
	    		featuresList.append( dataset[i][-1] )
	    for i in range( lenghtOfTrainingSet, len(dataset) ):
	    	testSet.append( dataset[i] )
	    	if dataset[i][-1] not in featuresList:
	    		featuresList.append( dataset[i][-1] )

	return (trainingSet, testSet)



def euclideanDist( x, y):
	dist = 0;

	import math;
	for i in range(len(x)-1):
		dist = dist + math.pow( (float(x[i])-float(y[i])), 2 );
	return math.sqrt(dist);



def getDistancesOfKSimilarSets( train, testInstance, k):
	
	distanes = []
	for i in range(len(train)):
		distanes.append( ( train[i], euclideanDist(train[i], testInstance) ) )
	
	import operator;
	distanes.sort( key=operator.itemgetter(1) );

	return [ item[0] for item in distanes[0:k] ];



def getPrediction( distOfkSimiarSets ):
	votesForTheClass = { }
	for item in distOfkSimiarSets:
		if item in votesForTheClass.keys():
			votesForTheClass[ item[-1] ] += 1;
		else:
			votesForTheClass[ item[-1] ] = 1;
	import operator
	l = sorted( votesForTheClass.iteritems(), key=operator.itemgetter(1), reverse=False )


	return l[0][0];



def get_1NN( train, testSet ):
	totalCount = len(testSet)
	OneNN = [];

	import operator;
	for i in range(len(testSet)):
		OneNN.append( getDistancesOfKSimilarSets( train, testSet[i], 1)[0] )

	return OneNN;



def getAuccuracy( train, testSet, k ):
	totalCount = len(testSet)
	correctCount = 0.0;

	# Init ConfusionMatrix
	confusionMatrix = { }
	for i in featuresList:
		for j in featuresList:
			confusionMatrix[ (i,j) ] = 0

	for i in range(len(testSet)):
		predition = getPrediction( getDistancesOfKSimilarSets( train, testSet[i], k ) )
		if predition == testSet[i][-1]:
			correctCount+=1;
		confusionMatrix[ testSet[i][-1], predition ] += 1

	print "Confusion Matrix"
	from texttable import Texttable
	table=[]
	row=[""]
	row.extend(featuresList)
	table.append(row)
	for i in featuresList:
		row=[i]
		for j in featuresList:
			row.append( confusionMatrix[ (i,j) ])
		table.append(row)
	T=Texttable();
	T.add_rows(table)
	print T.draw();

	return correctCount*1.0/totalCount;


""" python Iris_Solution.py <sizeOfTrainingSet[0-1]> <k> <DataSetFileName>
"""
def doKthNearestNeighbourClassification( filename, numberOfFeatures, fractionForTrainingSet, k ):

	(trainingSet, testSet) = loadDatasetRandSampling( filename, numberOfFeatures, fractionForTrainingSet )

	# print "Train set: " +str(len(trainingSet))
	# print "Test set: " +str(len(testSet))
	return getAuccuracy( trainingSet, testSet, k )