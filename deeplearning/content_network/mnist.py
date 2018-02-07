import numpy as np

from keras.datasets import mnist
from matplotlib import pyplot as plt
from keras.utils import np_utils
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras import losses

(X_train, y_train), (X_test, y_test) = mnist.load_data()

# plt.imshow(X_train[0])

X_train = X_train.reshape(X_train.shape[0], 1, 28, 28)
X_test = X_test.reshape(X_test.shape[0], 1, 28, 28)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

X_train /= 255
X_test /= 255

Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(1, 28, 28), activation='relu', data_format='channels_first'))

print(model.output_shape)

model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.compile(loss=losses.categorical_crossentropy,
              optimizer='adam',
              metrics=['accuracy'])

# model.fit(X_train, Y_train,
#           batch_size=32, epochs=10, verbose=1)

# score = model.evaluate(X_test, Y_test, verbose=0)
# print(score)
