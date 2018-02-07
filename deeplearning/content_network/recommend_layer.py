import numpy as np
from keras.models import Sequential
from keras.layers import Embedding
from keras.layers import Conv1D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras import losses
from keras.preprocessing.sequence import pad_sequences
from gensim.models import FastText
from pprint import pprint

with open('data_noun_token.vec', 'r', encoding="utf-8") as f:
    data = f.readlines()

word_vectors = {}
samples, dim = data[0].split()
samples, dim = int(samples), int(dim)

for line in data[1:]:
    word, vec = line.split(' ', 1)
    #     word = word.encode('utf-8')
    word_vectors[word] = np.array([
        float(i) for i in vec.split()
    ], dtype='float32')

E = np.zeros(shape=(int(samples), int(dim)), dtype='float32')
word_index = list(word_vectors.keys())

for ix in range(len(word_index)):
    word = word_index[ix]
    #     word_encode = word_index[ix].encode(('utf-8'))
    vec = word_vectors[word]
    for j in range(int(dim)):
        E[ix][j] = vec[j]

window_size = 10000
embedding = Embedding(
    100,
    32,
    weights=[E],
    input_length=window_size,
    trainable=False
)
# https://gist.github.com/brandonrobertz/49424db4164edb0d8ab34f16a3b742d5


trained_model = FastText.load_fasttext_format('data_noun_token')

input_train = []

fin = open('data_noun_token.txt', 'r')
lines = fin.readlines()
print(len(lines))
for line in lines:
    word_vector = []
    for word in line.split():
        try:
            word_vector.append(trained_model[word])
        except:
            pass
    input_train.append(word_vector)
fin.close()

input_train = pad_sequences(input_train, maxlen=int(100))
# input_train = np.array(input_train)
print(input_train.shape)
# print(input_train[0])

input_train = input_train.reshape(input_train.shape[0], 10000)
print(input_train.shape)

output_train = []
fbout = open('data_belong_label.txt', 'r')
lines = fbout.readlines()
for line in lines:
    lists = [int(x) for x in line.split(" ")]
    output_train.append(lists)
#     output_train.append(line.split(" "))
output_train = np.array(output_train)
fbout.close()
print(output_train.shape)
print(output_train[0:2])

model = Sequential()
model.add(embedding)
model.add(Conv1D(64, 3, padding='same', activation='relu'))
model.add(Conv1D(32, 3, padding='same', activation='relu'))
model.add(Conv1D(16, 3, padding='same', activation='relu'))
model.add(Flatten())
model.add(Dropout(0.2))
model.add(Dense(180, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(29, activation='sigmoid'))
model.compile(loss=losses.categorical_crossentropy,
              optimizer='adam',
              metrics=['accuracy'])

model.fit(input_train, output_train,
          batch_size=32, epochs=29, verbose=1)

trained_model = FastText.load_fasttext_format('data_noun_token')

print(trained_model['학습'])

tm = trained_model

tm.most_similar("장학금")
