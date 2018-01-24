import numpy as np
import pandas as pd

def pearson_similarity(vector1, vector2):
    return np.corrcoef(vector1, vector2)[0][1]

u_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
user_df = pd.read_csv('ml-latest-small/ratings.csv', sep=',', names=u_cols, encoding='utf-8', header=1)

print(user_df.shape)
# print(user_df.dtypes)
print(user_df.head())

user_num = user_df['user_id'].max()
movie_num = user_df['movie_id'].max()
rating_max = user_df['rating'].max()

df = user_df.loc[user_df['user_id'] == 1]
print(df)

print(df[['movie_id', 'rating']])

print((user_num, movie_num, rating_max))


class User:
    def __init__(self, index, rating_array):
        self.content_rating = rating_array
        # self.content_rating = np.random.randint(0, 4, num_contents)
        self.index = index

    def cal_similarity(self, another_user):
        return pearson_similarity(self.content_rating, another_user.content_rating)

    def __str__(self):
        return str(self.content_rating)

    def __repr__(self):
        return self.content_rating

    def score_item(self, all_user_similarity, item_index, users):
        x = 0.0
        y = np.sum(all_user_similarity[self.index])
        for user in users:
            if user.content_rating[item_index] == 0:
                pass
            else:
                x = x + all_user_similarity[self.index][user.index]
        return x / y

    def shape(self):
        return self.content_rating.shape

users = []
for i in range(1, user_num+1):
    df = user_df.loc[user_df['user_id'] == 1]
    user = User(i, )


# label_based 먼저 하러 중단..