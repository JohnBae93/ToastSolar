import numpy as np
from keras.layers import Embedding

class ToastEmbeddingLayer:
    _embedding_layer = None

    def __init__(self):
        f = open('../wiki.ko.vec', 'r')
        data = f.readlines()

        word_vectors = {}
        num_words, dim = data[0].split()  # (6, 300)
        num_words, dim = int(num_words), int(dim)
        print((num_words, dim))

        for line in data[1:]:
            word, vec = line.split(' ', 1)
            word_vectors[word] = np.array([
                float(i) for i in vec.split()
            ], dtype=np.float32)

        embedding_matrix = np.zeros(shape=(num_words, dim), dtype=np.float32)
        word_index = list(word_vectors.keys())
        print(len(word_index))
        for i in range(len(word_index)):
            word = word_index[i]
            vec = word_vectors[word]
            for j in range(int(dim)):
                embedding_matrix[i][j] = vec[j]

        window_size = 1

        self._embedding_layer = Embedding(
            input_dim=len(word_index),
            output_dim=int(dim),
            weights=[embedding_matrix],
            input_length=window_size
        )

    def embedding_layer(self):
        return self._embedding_layer
