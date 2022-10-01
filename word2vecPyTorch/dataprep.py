from utilities import scoreFunction, cosineSimilarity
import collections
import numpy as np
import os
import random
import math
from six.moves import xrange

dataIndex = 0


class DataPrep(object):
    def __init__(self, datafile, vocabLen):
        self.vocabLen = vocabLen
        self.pathToTemp = "temp"
        self.vocab = self.loadData(datafile)
        dataOr, self.count, self.vocabWords = self.buildDataset(self.vocab, self.vocabLen)
        self.trainData = self.subSampling(dataOr)
        # self.trainData = dataOr

        self.sampleTable = self.initSampleTable()

        self.saveVocab()

    def loadData(self, fileName):
        with open(fileName) as f:
            data = f.read().split()
        #       data = [x for x in data if x != 'eoood']
        return data

    def buildDataset(self, words, n_words):
        """Process given data"""
        count = [['unk', -1]]
        # most commond words of vacab size
        count.extend(collections.Counter(words).most_common(n_words - 1))
        dictionary = dict()
        for word, _ in count:
            dictionary[word] = len(dictionary)
        data = list()
        # new/unknow words counting
        unkCount = 0
        for word in words:
            if word in dictionary:
                index = dictionary[word]
            else:
                index = 0  # dictionary['UNK']
                unkCount += 1
            data.append(index)
        count[0][1] = unkCount
        reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
        return data, count, reversed_dictionary

    def saveVocab(self):
        """"save vocab to disk"""
        with open(os.path.join(self.pathToTemp, "vocab.txt"), "w") as f:
            for i in xrange(len(self.count)):
                vocab_word = self.vocabWords[i]
                f.write("%s %d\n" % (vocab_word, self.count[i][1]))

    def initSampleTable(self):
        count = [ele[1] for ele in self.count]
        powFrequency = np.array(count) ** 0.75
        power = sum(powFrequency)
        ratio = powFrequency / power
        table_size = 1e8
        count = np.round(ratio * table_size)
        sampleTable = []
        for idx, x in enumerate(count):
            sampleTable += [idx] * int(x)
        return np.array(sampleTable)

    def weightTable(self):
        count = [ele[1] for ele in self.count]
        powFrequency = np.array(count) ** 0.75
        power = sum(powFrequency)
        ratio = powFrequency / power
        return np.array(ratio)

    def subSampling(self, data):
        count = [ele[1] for ele in self.count]
        frequency = np.array(count) / sum(count)
        P = dict()
        for idx, x in enumerate(frequency):
            y = (math.sqrt(x / 0.001) + 1) * 0.001 / x
            P[idx] = y
        subSampledData = list()
        for word in data:
            if random.random() < P[word]:
                subSampledData.append(word)
        return subSampledData

    def batchGeneration2(self, skipWindow, batchSize):
        global dataIndex
        data = self.trainData
        batch = np.ndarray(shape=(batchSize), dtype=np.int64)
        labels = np.ndarray(shape=(batchSize, 2 * skipWindow), dtype=np.int64)
        span = 2 * skipWindow + 1  # [ skipWindow target skipWindow ]
        buffer = collections.deque(maxlen=span)

        if dataIndex + span > len(data):
            dataIndex = 0
        buffer.extend(data[dataIndex:dataIndex + span])
        dataIndex += span
        for i in range(batchSize):
            batch[i] = buffer[skipWindow]
            targets = [x for x in range(skipWindow)] + [x for x in range(skipWindow + 1, span)]
            for idj, j in enumerate(targets):
                labels[i, idj] = buffer[j]
            if dataIndex == len(data):
                buffer.extend(data[:span])
                dataIndex = span
                self.process = False
            else:
                buffer.append(data[dataIndex])
                dataIndex += 1
        # Backtrack a little bit to avoid skipping words in the end of a batch
        dataIndex = (dataIndex + len(data) - span) % len(data)
        return batch, labels

    def batchGeneration1(self, windowSize, batchSize, count):
        data = self.trainData
        global dataIndex
        span = 2 * windowSize + 1
        context = np.ndarray(shape=(batchSize, 2 * windowSize), dtype=np.int64)
        labels = np.ndarray(shape=(batchSize), dtype=np.int64)
        pos_pair = []

        if dataIndex + span > len(data):
            dataIndex = 0
            self.process = False
        buffer = data[dataIndex:dataIndex + span]
        pos_u = []
        pos_v = []

        for i in range(batchSize):
            dataIndex += 1
            context[i, :] = buffer[:windowSize] + buffer[windowSize + 1:]
            labels[i] = buffer[windowSize]
            if dataIndex + span > len(data):
                buffer[:] = data[:span]
                dataIndex = 0
                self.process = False
            else:
                buffer = data[dataIndex:dataIndex + span]

            for j in range(span - 1):
                pos_u.append(labels[i])
                pos_v.append(context[i, j])
        neg_v = np.random.choice(self.sampleTable, size=(batchSize * 2 * windowSize, count))
        return np.array(pos_u), np.array(pos_v), neg_v
