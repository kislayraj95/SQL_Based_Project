from word2vec import word2vec

#define parameters for generate embedding
vocabularySize=100000
embeddingDim=200
epochs=10
batchSize=16
windowSize=5
negSampleSize=10
# pathToData = 'data/text888.txt'
pathToData = 'data/text8.txt'

wc = word2vec(pathToData, vocabularySize=vocabularySize, embeddingDim=embeddingDim, epochs=epochs, batchSize=batchSize,
              windowSize=windowSize, negSampleSize=negSampleSize)
wc.train()