import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np

dictionary = np.load('dictionary.npy').tolist()
embeddings = np.load('embeddings.npy')
numDimensions = len(embeddings[0])
batchSize = 2
lstmUnits = 64
numClasses = 2
iterations = 10
maxSeqLength = 10

tf.reset_default_graph()

labels = tf.placeholder(tf.float32, [batchSize, numClasses])
input_data = tf.placeholder(tf.int32, [batchSize, maxSeqLength])

data = tf.Variable(tf.zeros([batchSize, maxSeqLength, numDimensions]),dtype=tf.float32)
data = tf.nn.embedding_lookup(embeddings ,input_data)

lstmCell = rnn.BasicLSTMCell(lstmUnits)
lstmCell = tf.contrib.rnn.DropoutWrapper(cell=lstmCell, output_keep_prob=0.75)
value, _ = tf.nn.dynamic_rnn(lstmCell, data, dtype=tf.float32)
weight = tf.Variable(tf.truncated_normal([lstmUnits, numClasses]))
bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))
value = tf.transpose(value, [1, 0, 2])
last = tf.gather(value, int(value.get_shape()[0]) - 1)
prediction = (tf.matmul(last, weight) + bias)
correctPred = tf.equal(tf.argmax(prediction,1), tf.argmax(labels,1))
accuracy = tf.reduce_mean(tf.cast(correctPred, tf.float32))
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=labels))
optimizer = tf.train.AdamOptimizer().minimize(loss)

sess = tf.InteractiveSession()
saver = tf.train.Saver()
sess.run(tf.global_variables_initializer())
def getTrainBatch():
    batch = [[2, 45, 654, 33, 345, 6665, 3, 5, 4, 654],[21, 425, 6524, 303, 3425, 16665, 4443, 35, 14, 11]]
    labels=[[0,1],[1,0]]
    return batch, labels

for i in range(iterations):
    nextBatch, nextBatchLabels = getTrainBatch()
    sess.run(optimizer, {input_data: nextBatch, labels: nextBatchLabels})

