import numpy as np
from keras.models import Sequential
from keras.layers import Embedding
from keras.layers import Conv1D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras import losses
from gensim.models import KeyedVectors
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split


NUM_ONCE_TRAIN = 1000
PADDING_MAXLEN = 500


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
print(output_train.shape)
fb.close()
fp.close()


'''INPUT DATA'''
trained_matrix = KeyedVectors.load_word2vec_format('../../data_noun_fasttext.vec', encoding='utf-8')
f = open('../../data_noun.txt', 'r')
lines = f.readlines()
f.close()
input_train = []
print(len(lines))
maxlen = 0
for line in lines:
    # print(line[0:5])
    length = 0
    word_vector = []
    for word in line.split():
        try:
            if len(word) == 1:    # 한글자 단어 제외
                continue
            length += 1
            word_vector.append(trained_matrix[word])
        except:
            pass
    maxlen = max(maxlen, length)
    input_train.append(word_vector)

print(maxlen)


'''MODEL'''
model = Sequential()
model.add(Conv1D(64, 3, input_shape=(None, 100), activation='relu'))
model.add(Conv1D(32, 3, padding='same', activation='relu'))
model.add(Conv1D(16, 3, padding='same', activation='relu'))
model.add(Flatten())
model.add(Dropout(0.2))
model.add(Dense(180, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(43, activation='sigmoid'))
model.compile(loss=losses.categorical_crossentropy,
              optimizer='adam',
              metrics=['accuracy'])


'''SPLIT DATA'''
x_train, x_test, y_train, y_test = train_test_split(input_train, output_train, test_size=0.2, random_state=42)
x_len = len(x_train)
print(x_len)
i = 0
while i < x_len:
    x = x_train[i:i+NUM_ONCE_TRAIN]
    y = y_train[i:i+NUM_ONCE_TRAIN]
    model.fit(x, y, batch_size=32, epochs=5, verbose=1)
    print(i)
    i += NUM_ONCE_TRAIN


# input_train = pad_sequences(input_train, maxlen=500)
# print(input_train.shape)

score = model.evaluate(x_test, y_test)
print(score)


n