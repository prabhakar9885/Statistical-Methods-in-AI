#!/bin/python

featuresList = range(10);


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



def euclideanDist(x, y):
    dist = 0;

    import math;
    for i in range(len(x) - 1):
        dist = dist + math.pow((float(x[i]) - float(y[i])), 2);
    return math.sqrt(dist);



def getDistancesOfKSimilarSets(train, testInstance, k):
    
    distanes = []
    for i in range(len(train)):
        distanes.append((train[i], euclideanDist(train[i], testInstance)))
    
    import operator;
    distanes.sort(key=operator.itemgetter(1));

    return [ item[0] for item in distanes[0:k] ];



def getPrediction(distOfkSimiarSets):
    votesForTheClass = { }
    for item in distOfkSimiarSets:
        if item in votesForTheClass.keys():
            votesForTheClass[ item[-1] ] += 1;
        else:
            votesForTheClass[ item[-1] ] = 1;
    import operator
    l = sorted(votesForTheClass.iteritems(), key=operator.itemgetter(1), reverse=False)


    return l[0][0];



def get_1NN(train, testSet):
    totalCount = len(testSet)
    OneNN = [];

    import operator;
    for i in range(len(testSet)):
        OneNN.append(getDistancesOfKSimilarSets(train, testSet[i], 1)[0])

    return OneNN;



def getAuccuracy(train, testSet, k):
    totalCount = len(testSet)
    correctCount = 0.0;

    # Init ConfusionMatrix
    confusionMatrix = { }
    for i in featuresList:
        for j in featuresList:
            confusionMatrix[ (i, j) ] = 0

    print("Applying KNN with K:" + str(k))
    for i in range(len(testSet)):
        predition = getPrediction(getDistancesOfKSimilarSets(train, testSet[i], k))
        if predition == testSet[i][-1]:
            correctCount += 1;
        confusionMatrix[ testSet[i][-1], predition ] += 1
    print("Done")

    for i in featuresList:
        print ("{:20}".format(i)),
        for j in featuresList:
            print ("{:4}".format(confusionMatrix[ (i, j) ])),
        print ("");

    return correctCount / totalCount;




""" python Iris_Solution.py <sizeOfTrainingSet[0-1]> <k> <DataSetFileName>
"""
def doKthNearestNeighbourClassification(filename, numberOfFeatures, fractionForTrainingSet, k):

    print("Loading the Dataset..")
    (trainingSet, testSet) = loadDatasetRandSampling(filename, numberOfFeatures, fractionForTrainingSet)
    print("Done")


    # print "Train set: " +str(len(trainingSet))
    # print "Test set: " +str(len(testSet))
    return getAuccuracy(trainingSet, testSet, k)


from array import array as pyarray
from numpy import append, array, int8, uint8, zeros, dtype
import os, struct
import timeit
import pickle

import numpy as np

def load_mnist(dataset="training", digits=np.arange(10), path="."):
    '''
    Load the training data-set and the labels
    '''
    if dataset == "training":
        fname_img = os.path.join(path, 'train-images.idx3-ubyte')
        fname_lbl = os.path.join(path, 'train-labels.idx1-ubyte')
    elif dataset == "testing":
        fname_img = os.path.join(path, 't10k-images.idx3-ubyte')
        fname_lbl = os.path.join(path, 't10k-labels.idx1-ubyte')
    else:
        raise ValueError("dataset must be 'testing' or 'training'")

    flbl = open(fname_lbl, 'rb')
    magic_nr, size = struct.unpack(">II", flbl.read(8))
    lbl = pyarray("b", flbl.read())
    flbl.close()

    fimg = open(fname_img, 'rb')
    magic_nr, size, rows, cols = struct.unpack(">IIII", fimg.read(16))
    img = pyarray("B", fimg.read())
    fimg.close()

    ind = [ k for k in range(size) if lbl[k] in digits ]
    N = len(ind)

    images = zeros((N, rows, cols), dtype=uint8)
    labels = zeros((N, 1), dtype=int8)
    for i in range(1000):  # len(ind)):
        images[i] = array(img[ ind[i] * rows * cols : (ind[i] + 1) * rows * cols ]).reshape((rows, cols))
        labels[i] = lbl[ind[i]]

    return images, labels      


'''
Load the data-set into a file with format < 768-pixel-values, label > 
'''

images, labels = load_mnist(path="/home/prabhakar/IIIT-H_current/Sem 2/SMAI/Ass3_DataSet/")
countOfImages = labels.shape[0]
fileObj = open("digits.csv", "w+")

for i in range(countOfImages):
    img = images[i]
    img[img > 0] = 1 
    line = str(img.tolist()).replace("[", "").replace("]", "")
    line += str("," + str(labels[i]).replace("[", "").replace("]", "").replace(" ", "") + "\n")
    fileObj.write(line)
    
fileObj.close()

doKthNearestNeighbourClassification("digits.csv", 784, 0.8, 1)
