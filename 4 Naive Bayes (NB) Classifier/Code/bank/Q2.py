#!/bin/python

import sys
import csv
import operator
import numpy as np
import random as r
import pickle as p

filename = sys.argv[1]

print filename

def loadDataset(filename, enableFrequency = False):
	featuresForClass = {}
	with open(filename, 'rb') as csvfile:
		lines = csv.reader(csvfile)
		for line in lines:
			words = line
			classNumber = words[-1]
			features =  [ i for i in words[:-1] ]
			if classNumber in featuresForClass.keys():
				featuresForClass[classNumber] = np.vstack( (featuresForClass[classNumber], features) )
			else:
				featuresForClass[classNumber] = np.array( np.array(features) )

	if enableFrequency == False:
		return featuresForClass

	# Features falling under class-"yes"
	cy =[]
	for i in range( len( featuresForClass['yes'][0] ) ):
		f = featuresForClass['yes'][:, i].tolist()
		cy.append( { x:f.count(x) for x in f }  )

	# Features falling under class-"no"
	cn =[]
	for i in range( len( featuresForClass['no'][0] ) ):
		f = featuresForClass['no'][:, i].tolist()
		cn.append( { x:f.count(x) for x in f }  )

	featuresForClass = {}

	featuresForClass['yes'] = cy
	featuresForClass['no'] = cn

	return featuresForClass


def getMeanAndSDbyClassNumber(featuresForClass):
	meanForClass = {}
	SDForClass = {}

	for classNumber in featuresForClass.keys():
		features = featuresForClass[classNumber]
		for feature in range( len(features) ):
			if classNumber in meanForClass:
				meanForClass[classNumber].append( np.mean([ features[feature][i] for i in features[feature].keys() ]) )
			else:
				meanForClass[classNumber] = [ np.mean([ features[feature][i] for i in features[feature].keys() ]) ]
			if classNumber in SDForClass:
				SDForClass[classNumber].append( np.std([ features[feature][i] for i in features[feature].keys() ]) )
			else:
				SDForClass[classNumber] = [ np.std([ features[feature][i] for i in features[feature].keys() ]) ]

	return meanForClass, SDForClass


def getProbabilityForFeaturesGivenClass( featuresForClass ):
	probabilities = {}

	for classNumber in featuresForClass.keys():
		featuresListForTheClass = featuresForClass[classNumber]
		for features in featuresListForTheClass:
			denomForProbabilty = np.sum( [ features[i] for i in features.keys()] )
			probabilityForFeatures = \
					{ i: (1+features[i])*1.0 / (denomForProbabilty+len(featuresForClass)) for i in features.keys() }
			if classNumber in probabilities:
				probabilities[classNumber].append( probabilityForFeatures )
			else:
				probabilities[classNumber] = [ probabilityForFeatures ]

	return probabilities

 	
def getProbabilityForClass( featuresForClass ):
	p = {}
	totalNumberOfObservations = 0;
	numberOfObservationsInClass = {}

	for i in featuresForClass.keys():
		count = 0
		for features in featuresForClass[i]:
			count += np.sum([ features[feature] for feature in features.keys() ])
		numberOfObservationsInClass[ i ] = count
		totalNumberOfObservations += count

	for i in featuresForClass.keys():
		p[i] = numberOfObservationsInClass[ i ]*1.0/totalNumberOfObservations
	return p;


def predictClass( features, probabilityForClass, probabilityForFeaturesGivenClass ):
	probability = {}
	for classNumber in featuresForClass.keys():
		probability[classNumber] = 1
		for feature in range( len(features) ):
			probability[classNumber] += np.log10( probabilityForFeaturesGivenClass[classNumber][feature][features[feature]] )
		probability[classNumber] += np.log10( probabilityForClass[classNumber] )
	
	return max(probability.iteritems(), key=operator.itemgetter(1))[0]


def getConfusionMatrix( probabilityForFeaturesGivenClass, probabilityForClass, testSet ):
	confusionMatrix = {}
	for classNumber in probabilityForFeaturesGivenClass.keys():
		confusionMatrix[classNumber] = {};
		for i in probabilityForFeaturesGivenClass.keys():
			confusionMatrix[classNumber][i] = 0

	for classNumber in probabilityForFeaturesGivenClass.keys():
		for testRow in range( len(testSet[classNumber]) ):
			prediction = predictClass( testSet[classNumber][testRow], probabilityForClass, probabilityForFeaturesGivenClass )
			confusionMatrix[classNumber][prediction] += 1

	return confusionMatrix


print "Loading data with frequency..."
featuresForClass = loadDataset(filename, enableFrequency = True)
p.dump( featuresForClass, open("featuresForClass.dump", "wb+") )
print "done"

print "Loading data with frequency..."
probabilityForFeaturesGivenClass = getProbabilityForFeaturesGivenClass( featuresForClass )
print "done"

print "Computing the probabilities..."
probabilityForClass = getProbabilityForClass( featuresForClass )
print "done"

print "confusionMatrix: "
testSet = loadDataset(filename, enableFrequency = False)
p.dump( testSet, open("testSet.dump", "wb+") )
p.dump( probabilityForFeaturesGivenClass, open("prob.dump", "wb+") )
confusionMatrix = getConfusionMatrix(probabilityForFeaturesGivenClass, probabilityForClass, testSet)
for row in confusionMatrix:
	print confusionMatrix[row]


# Print Accuracy
correct = 0
total = 0
for row in confusionMatrix.keys():
	for col in confusionMatrix[row].keys():
		if col == row:
			correct += confusionMatrix[row][col]
		total += confusionMatrix[row][col]
print "Accuracy: " + str(100.0 * correct / total)

# randClassIndex = r.randint( 0, len(featuresForClass)-1 )
# randClass = featuresForClass.keys()[randClassIndex]
# randRowIndex = r.randint( 0, len(featuresForClass[randClass])-1 )
# features = featuresForClass[randClass][randRowIndex]

# print predictClass(features, probabilityForFeaturesGivenClass, featuresForClass )

