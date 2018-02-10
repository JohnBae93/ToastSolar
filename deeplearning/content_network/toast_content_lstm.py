import numpy as np
from keras.models import Sequential
from keras.layers import Embedding
from keras.layers import Conv1D, AveragePooling2D, Conv2D, RNN, LSTM
from keras.layers import Dense, Dropout, Activation, Flatten
from keras import losses
from gensim.models import KeyedVectors
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split


NUM_ONCE_TRAIN = 1000
PADDING_MAXLEN = 500

trained_matrix = KeyedVectors.load_word2vec_format('../../data_noun_fasttext.vec', encoding='utf-8')
# print(trained_matrix.most_similar('장학', topn=30))

input_file = '../../data_noun.txt'
belong_file = '../../data_belong_label.txt'
property_file = '../../data_property_label.txt'


'''OUTPUT DATA'''
fb = open(belong_file, 'r')
fp = open(property_file, 'r')

lines = fb.readlines()
length_data = len(lines)
length_label = 0

output_train = []
for line in lines:
    lists = [int(x) for x in line.split(" ")]
    lists += [int(x) for x in fp.readline().split(" ")]
    length_label = len(lists)
    output_train.append(lists)

# print(output_train)
output_train = np.array(output_train, dtype=np.int8)
output_train = np.reshape(output_train, (length_data, length_label))
print("output data shape {}".format(output_train.shape))
fb.close()
fp.close()


'''INPUT DATA'''
f = open(input_file, 'r')
lines = f.readlines()
f.close()
input_train = np.array([])
len_line = len(lines)
print("data line length: {}".format(len_line))

for line in lines:
    # print(line[0:5])
    word_vector = np.zeros((1,100), dtype=np.float32)
    for word in line.split():
        try:
            if len(word) == 1:    # 한글자 단어 제외
                continue
            # word_vector = np.append(word_vector, trained_matrix[word])
            word_vector = np.add(word_vector, trained_matrix[word])
        except:
            pass
    input_train = np.append(input_train, word_vector)
    # input_train = np.append(input_train, word_vector)

input_train = input_train.reshape((len_line, 1, 100))
print(input_train.shape)

'''MODEL'''
model = Sequential()
model.add(LSTM(120, input_shape=(1, 100)))
model.add(Dense(80, activation='relu'))
model.add(Dense(43, activation='sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


# input_train = input_train.reshape(input_train.shape[0], 1, 500, 100)
'''SPLIT DATA'''
x_train, x_test, y_train, y_test = train_test_split(input_train, output_train, test_size=0.2, random_state=42)
x_len = len(x_train)
print(x_len)
# x_train = np.array(x_train, dtype=np.int8)
# x_test = np.array(x_test, dtype=np.int8)

i = 0
while i < x_len:
    x = x_train[i:i+NUM_ONCE_TRAIN]
    y = y_train[i:i+NUM_ONCE_TRAIN]
    model.fit(x, y, batch_size=16, epochs=3, verbose=1, validation_data=(x_test, y_test))
    print(i)
    i += NUM_ONCE_TRAIN
# model.save('../../toast_lstm.h5')
model.save('../../toast_lstm_except_1word.h5')
score = model.evaluate(x_test, y_test)
print(score)

