#!/bin/python

featuresList = [];

def loadDatasetWithNFold( dataset, numberOfFeatures, startIndexForTestData, endIndexForTestData ):

    trainingSet=[]
    testSet=[]

    endIndexForTestData = endIndexForTestData if endIndexForTestData<len(dataset) else len(dataset)-1
    
    for i in range(startIndexForTestData+1):
        trainingSet.append( dataset[i] )
        if dataset[i][-1] not in featuresList:
            featuresList.append( dataset[i][-1] )

    for i in range(startIndexForTestData+1, endIndexForTestData+1):
    	testSet.append( dataset[i] )
	if dataset[i][-1] not in featuresList:
            featuresList.append( dataset[i][-1] )

    for i in range(startIndexForTestData+2, len(dataset)):
	trainingSet.append( dataset[i] )
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

	for i in range(len(testSet)):
		predition = getPrediction( getDistancesOfKSimilarSets( train, testSet[i], k ) )
		if predition == testSet[i][-1]:
			correctCount+=1;

	return correctCount*1.0/totalCount;



""" python driver_kFold_Sampling.py <k> <file-name> <feature-count>
"""
def doKthNearestNeighbourClassification( filename, numberOfFeatures, numberOfFolds, k ):

	auccuracy = 0;
	sum = 0
	squareSum = 0;

	import csv
	import random
	import math as m

	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    accuracyList =[]
	    for i in range(10):
	    	    print "--------------"
	   	    print "Trial: " +str(i+1)
	   	    random.shuffle( dataset )
		    numberOfLines = len(dataset)
		    foldSize = numberOfLines/(numberOfFolds-1)
		    currentFoldNum = 0;
                    sum=0
	   	    for i in range(0, numberOfLines, foldSize):
	                (trainingSet, testSet) = loadDatasetWithNFold( dataset, \
		    							    numberOfFeatures, \
										    i, \
										    i+foldSize-1 );
	                currentFoldNum +=1
	                val = getAuccuracy( trainingSet, testSet, k )
	                sum += val
	                squareSum += (sum*sum)
	                print "For Fold-" + str(currentFoldNum) + ": Accuracy-" + str(val*100)

	            mean = sum*1.0/(numberOfFolds);
	            accuracyList.append( mean );


        return accuracyList;
