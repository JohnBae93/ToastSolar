import numpy as np
import random
import matplotlib.pyplot as plt


def cosine_similarity(vector1, vector2):
    vector1_len = np.linalg.norm(vector1)
    vector2_len = np.linalg.norm(vector2)

    return np.dot(vector1, vector2) / (vector1_len * vector2_len)


def pearson_similarity(vector1, vector2):
    return np.corrcoef(vector1, vector2)[0][1]


print(cosine_similarity(np.array([1, 0]), np.array([-1, 0])))

num_contents = 10
num_users = 10


class User:
    def __init__(self, index, rating_array=None):
        if rating_array is None:
            self.content_rating = np.random.randint(0, 4, num_contents)
        else:
            self.content_rating = np.array(rating_array)
        self.index = index

    def cal_similarity(self, another_user):
        #         return cosine_similarity(self.content_rating, another_user.content_rating)
        return pearson_similarity(self.content_rating, another_user.content_rating)

    def __str__(self):
        return str(self.content_rating)

    def __repr__(self):
        return self.content_rating

    def score_item(self, _all_user_similarity, item_index, _users):
        x = 0.0
        y = np.sum(_all_user_similarity[self.index])
        for _user in _users:
            if _user.content_rating[item_index] == 0:
                pass
            else:
                x = x + _all_user_similarity[self.index][_user.index]
        return x / y

    def shape(self):
        return self.content_rating.shape


users = []
print(num_users)

user0 = User(0, [])
user1 = User(1, [])
user2 = User(2, [])
user3 = User(3, [])
user4 = User(4, [])
user5 = User(5, [])
user6 = User(6, [])
user7 = User(7, [])
user8 = User(8, [])
user9 = User(9, [])
# for j in range(0, num_users):
#     user = User(j, [])
#     users.append(user)

print(len(users))

np.set_printoptions(threshold=np.nan)
print(users[1].shape())
for user in users:
    print(user.index, end=" ")
    print(user)

all_user_similarity = np.zeros((num_users, num_users), dtype=np.float32)

for k in range(0, num_users):
    for l in range(0, k):
        if k == l:
            pass
        else:
            all_user_similarity[k][l] = users[k].cal_similarity(users[l])
            if abs(all_user_similarity[k][l]) < 0.00001:
                all_user_similarity[k][l] = 0.0
            all_user_similarity[l][k] = all_user_similarity[k][l]

print(all_user_similarity)

for i in range(0, 10):
    print(users[1].score_item(all_user_similarity, i, users))