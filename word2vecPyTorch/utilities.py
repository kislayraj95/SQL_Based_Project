import csv
from scipy.stats import spearmanr
import math


def cosineSimilarity(vector1, vector2):
    sumXX, sumXY, sumYY = 0, 0, 0
    for i in range(len(vector1)):
        x = vector1[i];
        y = vector2[i]
        sumXX += x * x
        sumYY += y * y
        sumXY += x * y
    return sumXY / math.sqrt(sumXX * sumYY)


def scoreFunction(embed):

    f = open('temp/vocab.txt')
    line = f.readline()
    vocab = []
    wordindex = dict()
    index = 0
    while line:
        word = line.strip().split()[0]
        wordindex[word] = index
        index = index + 1
        line = f.readline()
    f.close()
    ze = []
    with open('wordsim353/combined.csv') as csvfile:
        fileWordsSim353 = csv.reader(csvfile)
        index = 0
        consim = []
        humansim = []
        for eles in fileWordsSim353:
            if index == 0:
                index = 1
                continue
            if (eles[0] not in wordindex) or (eles[1] not in wordindex):
                continue

            firstWord = int(wordindex[eles[0]])
            secondWord = int(wordindex[eles[1]])
            humansim.append(float(eles[2]))

            value1 = embed[firstWord]
            value2 = embed[secondWord]
            index = index + 1
            score = cosineSimilarity(value1, value2)
            consim.append(score)

    corr, pvalue1 = spearmanr(humansim, consim)

    if 1 == 1:
        lines = open('rw/rw.txt', 'r').readlines()
        index = 0
        consim = []
        humansim = []
        for line in lines:
            eles = line.strip().split()
            if (eles[0] not in wordindex) or (eles[1] not in wordindex):
                continue
            firstWord = int(wordindex[eles[0]])
            secondWord = int(wordindex[eles[1]])
            humansim.append(float(eles[2]))
            value1 = embed[firstWord]
            value2 = embed[secondWord]
            index = index + 1
            score = cosineSimilarity(value1, value2)
            consim.append(score)
    # calculate spearman coefficient
    corr, pValue = spearmanr(humansim, consim)

    return corr, corr