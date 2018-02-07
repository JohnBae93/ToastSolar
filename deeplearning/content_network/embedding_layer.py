from __future__ import print_function
import numpy as np
from keras.models import Sequential
from keras.layers import Embedding

with open('../wiki.ko.vec', 'r') as f:
    data = f.readline()

word_vectors = {}
samples, dim = data.split()
print(dim)
print(len(samples))
#
# for line in data[1:]:
#     word, vec = line.split(' ', 1)
#     word_vectors[word] = np.array([
#         float(i) for i in vec.split()
#     ], dtype='float32')
#
# E = np.zeros(shape=(int(samples), int(dim)), dtype='float32')
# word_index = list(word_vectors.keys())
# for ix in range(len(word_index)):
#     word = word_index[ix]
#     vec = word_vectors[word]
#     for j in range(int(dim)):
#         E[ix][j] = vec[j]
#
# window_size = 1
# embedding = Embedding(
#     len(word_index),
#     int(dim),
#     weights=[E],
#     input_length=window_size,
#     trainable=False
# )
#
#
# model = Sequential()
# model.add(embedding)
# model.compile('sgd', 'mse', ['accuracy'])
#
# print( "Predicted embedding vector", p)
# print( "Actual embedding vector", a)
# print( "Equal?", p == a)