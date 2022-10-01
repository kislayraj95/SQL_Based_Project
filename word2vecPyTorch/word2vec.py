import zipfile
import collections
import numpy as np

import math
import random

import torch
import warnings
warnings.filterwarnings("ignore")
from torch.autograd import Variable
import torch.optim as optim
import time


from dataprep import DataPrep, scoreFunction
from model import skipgram


class word2vec:
    # initialize parameters
    def __init__(self, inputfile, vocabularySize=100000, embeddingDim=200, epochs=10, batchSize=16,
                 windowSize=5, negSampleSize=10):
        self.op = DataPrep(inputfile, vocabularySize)
        self.embeddingDim = embeddingDim
        self.windowSize = windowSize
        self.vocabularySize = vocabularySize
        self.batchSsize = batchSize
        self.epochs = epochs
        self.negSampleSize = negSampleSize

    def train(self):
        # create model
        model = skipgram(self.vocabularySize, self.embeddingDim)
        if torch.cuda.is_available():
            model.cuda()
        # optimizer that can be changed; many other are avaiable
        optimizer = optim.SGD(model.parameters(), lr=0.2)
        for epoch in range(self.epochs):
            start = time.time()
            self.op.process = True
            batch_num = 0
            batch_new = 0

            while self.op.process:
                pos_u, pos_v, neg_v = self.op.batchGeneration1(self.windowSize, self.batchSsize, self.negSampleSize)

                pos_u = Variable(torch.LongTensor(pos_u))
                pos_v = Variable(torch.LongTensor(pos_v))
                neg_v = Variable(torch.LongTensor(neg_v))

                if torch.cuda.is_available():
                    pos_u = pos_u.cuda()
                    pos_v = pos_v.cuda()
                    neg_v = neg_v.cuda()

                optimizer.zero_grad()
                loss = model(pos_u, pos_v, neg_v, self.batchSsize)

                loss.backward()

                optimizer.step()

                if batch_num % 30000 == 0:
                    torch.save(model.state_dict(), 'temp/skipgram.epoch{}.batch{}'.format(epoch, batch_num))

                if batch_num % 2000 == 0:
                    end = time.time()
                    word_embeddings = model.input_embeddings()
                    sp1, sp2 = scoreFunction(word_embeddings)
                    # print('eporch,batch=%2d, %5d: sp=%1.3f %1.3f  pair/sec = %4.2f loss=%4.3f\r' \
                    #       % (epoch, batch_num, sp1, sp2, (batch_num - batch_new) * self.batchSsize / (end - start),
                    #          loss.data.item()), end="")

                    print('eporch,batch=%2d, %5d: sp=%1.3f %1.3f   loss=%4.3f\r'  % (epoch, batch_num, sp1, sp2, loss.data.item()), end="")
                    batch_new = batch_num
                    start = time.time()
                batch_num = batch_num + 1
            print()
        print("Optimization Finished!")


# if __name__ == '__main__':
#     wc = word2vec('data/text8.txt')
#     wc.train()