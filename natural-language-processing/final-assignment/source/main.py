import numpy as np
import TweetsDataSet as td
import KerasNetwork as kn
import numpy as np
import Utils as ut
        
train_size = 21000
test_size = 9000
vector_size = 512
word2vecIterations = 50
max_length = 18
datasetFilePath = 'dataset/emotions_tweets.csv'

np.random.seed(1000)

print('Iniciando')

tweetsDataSet = td.TweetsDataSet(datasetFilePath, (train_size + test_size), train_size)
kerasModel = kn.KerasNetwork(max_length, vector_size, train_size, test_size, word2vecIterations, tweetsDataSet)

del train_size
del test_size
del vector_size
del word2vecIterations
del max_length
del datasetFilePath
del tweetsDataSet

for i in range(1,2):
    print('Teste com {} épocas'.format((i * 10)))
    kerasModel.TrainModel((i * 10))
    scores = kerasModel.getScores()
    print('Neural Accurracy: {}'.format(scores[1]))
    #ut.Utils.registerToFile('{};{}\n'.format((i * 10), scores[1]), 'csv', 'accuracyByEppochCount.csv')
    del kerasModel.model
    del kerasModel.KerasPredict

# kerasModel.TrainModel()

# analysis = {}

# analysis['bayes_success'] = 0
# analysis['bayes_error'] = 0
# analysis['neural_success'] = 0
# analysis['neural_error'] = 0

# bayesPredict = bayes.getBayesPredict()
# neuralPredict = kerasModel.KerasPredict

# for i in range(0, test_size):
#     tweetClass = tweetsDataSet.bayes_test[i][1]
    
#     bayesClass = 0 if bayesPredict[i][1] > bayesPredict[i][0] else 1
#     neuralClass = 0 if neuralPredict[i][1] > neuralPredict[i][0] else 1

#     if (bayesClass == tweetClass):
#         analysis['bayes_success']+=1
#     else:
#         analysis['bayes_error']+=1
    
#     if (neuralClass == tweetClass):
#         analysis['neural_success']+=1
#     else:
#         analysis['neural_error']+=1

# print('bayes_success count: {}'.format(analysis['bayes_success']))
# print('bayes_error count: {}'.format(analysis['bayes_error']))
# print('neural_success count: {}'.format(analysis['neural_success']))
# print('neural_error count: {}'.format(analysis['neural_error']))


# scores = kerasModel.getScores()
# print('Neural Accurracy: {}'.format(scores[1]))