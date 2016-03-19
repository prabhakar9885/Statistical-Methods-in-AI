#!/bin/python

import sys
import csv
import numpy as np
import random as r

filename = sys.argv[1]

print filename

def loadDataset(filename):
	featuresForClass = {}
	with open(filename, 'rb') as csvfile:
		lines = csv.reader(csvfile)
		for line in lines:
			words = line
			classNumber = words[-1]
			features =  [ int(i) for i in words[1:-1] ]
			if classNumber in featuresForClass.keys():
				featuresForClass[classNumber] = np.vstack( (featuresForClass[classNumber], features) )
			else:
				featuresForClass[classNumber] = np.array( np.array(features) )

	return featuresForClass


def getMeanAndSDbyClassNumber(featuresForClass):
	meanForClass = {}
	SDForClass = {}

	for classNumber in featuresForClass.keys():
		features = featuresForClass[classNumber]
		for feature in range( len(features[0]) ):
			if classNumber in meanForClass:
				meanForClass[classNumber].append( np.mean(features[:,feature]) )
			else:
				meanForClass[classNumber] = [ np.mean(features[:,feature]) ]
			if classNumber in SDForClass:
				SDForClass[classNumber].append( np.std(features[:,feature]) )
			else:
				SDForClass[classNumber] = [ np.std(features[:,feature]) ]

	return meanForClass, SDForClass


def getGaussianNaiveBayes( x, mean, sd ):
	return 1/( np.sqrt(2*np.pi) * sd) * np.exp( -0.5 * np.power(x-mean, 2) / sd )


def getProbabilityForFeaturesGivenClass( featuresForClass, meanForClass, SDForClass ):
	probabilities = {}

	for classNumber in featuresForClass.keys():
		featuresListForTheClass = featuresForClass[classNumber]
		for features in featuresListForTheClass:
			probabilityForFeatures = \
					getGaussianNaiveBayes( features, np.array(meanForClass[classNumber]), np.array(SDForClass[classNumber]) )
			if classNumber in probabilities:
				probabilities[classNumber].append( probabilityForFeatures )
			else:
				probabilities[classNumber] = [ probabilityForFeatures ]

	return probabilities


def getProbabilityForClass( featuresForClass ):
	p = {}
	totalNumberOfObservations = 0;

	for i in featuresForClass.keys():
		totalNumberOfObservations += len(featuresForClass[i])

	for i in featuresForClass.keys():
		p[i] = len(featuresForClass[i])*1.0/totalNumberOfObservations
	return p;

def predictClass( features, featuresForClass ):
	probability = {}
	for classNumber in featuresForClass.keys():
		probability[classNumber] = np.prod(getGaussianNaiveBayes( np.array(features), \
											np.array(meanForClass[classNumber]), np.array(SDForClass[classNumber]) ) *\
											probabilityForClass[classNumber] );

	normalizingSum = 0
	for classNumber in featuresForClass.keys():
		normalizingSum += probability[classNumber]

	# Applied Log10 while calculating the probability
	for classNumber in featuresForClass.keys():
		probability[classNumber] = np.log10( probability[classNumber] / normalizingSum )

	maximumProbableClass = -1;
	for classNumber in featuresForClass.keys():
		if maximumProbableClass==-1 or probability[maximumProbableClass] < probability[classNumber]:
			maximumProbableClass = classNumber

	return maximumProbableClass;

def getConfusionMatrix( featuresForClass ):
	confusionMatrix = {}
	for classNumber in featuresForClass.keys():
		confusionMatrix[classNumber] = {};
		for feature in featuresForClass.keys():
			confusionMatrix[classNumber][feature] = 0
		for features in featuresForClass[classNumber]:
			confusionMatrix[classNumber][predictClass( features, featuresForClass )] += 1

	return confusionMatrix



featuresForClass = loadDataset(filename)
meanForClass, SDForClass = getMeanAndSDbyClassNumber( featuresForClass )

probabilityForFeaturesGivenClass = getProbabilityForFeaturesGivenClass( featuresForClass, meanForClass, SDForClass )
probabilityForClass = getProbabilityForClass( featuresForClass )

print "confusionMatrix: "
confusionMatrix = getConfusionMatrix(featuresForClass)
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

# print predictClass(features, featuresForClass)

