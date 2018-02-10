import numpy as np
import matplotlib.pyplot as plt
import json
import re
from keras import models
from konlpy.tag import Twitter
from gensim.models import KeyedVectors

major_urls = ["scos.skku", "liberalarts.skku", "law.skku", "sscience.skku", "ecostat.skku",
              "biz.skku", "coe.skku", "art.skku", "cscience.skku", "icc.skku", "cs.skku",
              "shb.skku", "pharm.skku", "biotech.skku", "sport.skku", "skkumed.skku", "icon.skku"]

major_names = ['유학', '문과', '법과', '사회과학', '경제', '경영', '사범', '예술', '자연과학', '정보통신', '소프트웨어', '공과', '약학', '생명공학', '스포츠과학',
               '의과', '융합']

belong_json_file = '../content_belong_label_keyword.json'
property_json_file = '../content_property_label_keyword.json'
data_file = '../data_small.txt'
user_file = '../users.txt'

def pearson_similarity(vector1, vector2):
    return np.corrcoef(vector1, vector2)[0][1]


def cosine_similarity(vector1, vector2):
    vector1_len = np.linalg.norm(vector1)
    vector2_len = np.linalg.norm(vector2)

    return np.dot(vector1, vector2) / (vector1_len * vector2_len)


def if_letters_in_content(letters, content):
    if any(s in content for s in letters):
        return True
    return False


def load_data(filename):
    file_content = open(filename).read()
    data_list = json.loads(file_content)
    data_list.sort(key=lambda x: x["label"])
    return data_list


class Curation:
    def __init__(self, belong_data, property_data, line):
        self.belong_label = np.zeros(len(belong_data), dtype=np.uint8)
        self.property_label = np.zeros(len(property_data), dtype=np.uint8)

        self._labelling(belong_data, property_data, line)
        self.label = np.concatenate((self.belong_label, self.property_label))
        self._predict(line)

    def _labelling(self, belong_data, property_data, line):
        for i, data in enumerate(belong_data):
            if self._check_keywords(data, line):
                self.belong_label[i] = 1

        for i, data in enumerate(property_data):
            if self._check_keywords(data, line):
                self.property_label[i] = 1

    def _check_keywords(self, data, line):
        try:
            diff_mode = data["keywords"]["type"]
        except Exception as e:
            print(data)
            raise Exception("Cannot read keyword type at data {}".format(data))

        p_match_word = re.compile(r"[가-힣A-Za-z0-9]")

        for keyword in data["keywords"]["list"]:
            if diff_mode == "EXACT":
                if keyword in line:
                    return True
            elif diff_mode == "INCLUDE_LETTER":
                new_line = "".join(p_match_word.findall(line))
                new_keyword = "".join(p_match_word.findall(keyword))
                if new_keyword in new_line:
                    return True
        return False

    def _predict(self, line):
        if self.label.max() <= 0:
            model = models.load_model('../toast_lstm_except_1word.h5')
            twiter = Twitter()
            trained_matrix = KeyedVectors.load_word2vec_format('../data_noun_fasttext.vec', encoding='utf-8')
            input = np.zeros((1, 100), dtype=np.float32)
            for word in twiter.nouns(line):
                try:
                    input = np.add(input, trained_matrix[word])
                except:
                    pass
            input = input.reshape(1,1,100)
            self.label = model.predict(input).reshape(43,)
        else:
            return

    def __str__(self):
        return " ".join(self.label)


class User:
    def __init__(self, _majors, _semester, _attend, _gender, _label_list):
        self.label = np.zeros(len(_label_list), dtype=np.float32)

        self.majors = _majors
        self.semester = int(_semester)
        self.attend = _attend
        self.gender = _gender

        self.labelling_belong(_label_list)
        self.labeling_property(_label_list)

    def labelling_belong(self, _label_list):
        for major in self.majors:
            for name in major_names:
                if name in major:
                    self.label[_label_list.index(name)] = 1

        if 1 <= self.semester <= 8:
            self.label[_label_list.index("{}학기".format(self.semester))] = 1
        else:
            self.label[_label_list.index("초과학기")] = 1

        if self.attend == '예':
            self.label[_label_list.index("재학생")] = 1
        elif self.attend == '아니오':
            self.label[_label_list.index("휴학생")] = 1

        if self.semester >= 7:
            self.label[_label_list.index("초과학기")] = 1


    def labeling_property(self, _label_list):
        # 1학년
        if self.semester == 1 or self.semester == 2:
            self.label[_label_list.index("학사일정")] = 1
            self.label[_label_list.index("여행")] = 1
            self.label[_label_list.index("국내봉사")] = 1
            self.label[_label_list.index("해외봉사")] = 1
            self.label[_label_list.index("기자단")] = 1
        # 2학년
        elif self.semester == 3 or self.semester == 4:
            self.label[_label_list.index("장학금")] = 1
            self.label[_label_list.index("대외활동")] = 1
            self.label[_label_list.index("학사일정")] = 1
            self.label[_label_list.index("강연")] = 1
            self.label[_label_list.index("여행")] = 1
            self.label[_label_list.index("국내봉사")] = 1
            self.label[_label_list.index("해외봉사")] = 1
            self.label[_label_list.index("기자단")] = 1
        # 3학년
        elif self.semester == 5 or self.semester == 6:
            self.label[_label_list.index("장학금")] = 1
            self.label[_label_list.index("대외활동")] = 1
            self.label[_label_list.index("학사일정")] = 1
            self.label[_label_list.index("강연")] = 1
            self.label[_label_list.index("교환학생")] = 1
            self.label[_label_list.index("기자단")] = 1
            self.label[_label_list.index("마케터")] = 1
            self.label[_label_list.index("인턴")] = 1
        # 4학년
        elif self.semester == 7 or self.semester == 8:
            self.label[_label_list.index("대외활동")] = 1
            self.label[_label_list.index("대학원")] = 1
            self.label[_label_list.index("취업")] = 1
            self.label[_label_list.index("인턴")] = 1
            self.label[_label_list.index("학사일정")] = 1
        else:
            self.label[_label_list.index("대학원")] = 1
            self.label[_label_list.index("취업")] = 1
            self.label[_label_list.index("인턴")] = 1


'''Curation Labelling'''
belong_data = load_data(filename=belong_json_file)
property_data = load_data(filename=property_json_file)

label_list = []
for belong in belong_data:
    label_list.append(belong["label"])
for property in property_data:
    label_list.append(property["label"])
print(label_list)
label_list = tuple(label_list)


fr = open(data_file, 'r')
data_lines = fr.readlines()

curations = []
for line in data_lines:
    curation = Curation(belong_data, property_data, line)
    curations.append(curation)
fr.close()


'''User Labeling'''
fr = open(user_file, 'r')
user_lines = fr.readlines()
users = []
for line in user_lines:
    content = line.split(" ")
    user_majors = []
    user_majors.append(content[0])
    if content[1].isdigit() == False:
        user_majors.append(content[1])
        user_semester = content[2]
        if content[3] == '재학':
            user_attend = '예'
        else:
            user_attend = '아니오'
        if content[4] == '남자':
            user_gender = 'M'
        else:
            user_gender = 'F'

    else:
        user_semester = content[1]
        if content[2] == '재학':
            user_attend = '예'
        else:
            user_attend = '아니오'
        if content[3] == '남자':
            user_gender = 'M'
        else:
            user_gender = 'F'

    user = User(user_majors, user_semester, user_attend, user_gender, label_list)
    users.append(user)
fr.close()

user_num = len(users)
curation_num = len(curations)

print((user_num, curation_num))
# print(user)

# print(users[0].label)

similarity_matrix = np.zeros((user_num, curation_num), dtype=np.float32)
print(similarity_matrix.shape)

for i, user in enumerate(users):
    for j, curation in enumerate(curations):
        similarity_matrix[i][j] = pearson_similarity(user.label,
                                                     curation.label)


for i in range(0, user_num):
    print(("user {}:".format(i + 1), similarity_matrix[i].max(), np.argmax(similarity_matrix[i]) + 1))
    for j in range(0, curation_num):
        score = similarity_matrix[i][j]
        if score > 0.6:
            print("user : {} , curation : {}, score : {}, text : {} ".format(i + 1, j + 1, similarity_matrix[i][j],
                                                                             data_lines[j][12:40]))

np.set_printoptions(threshold=5000, precision=2)
# print(similarity_matrix)
print(similarity_matrix.mean())
similarity_matrix_1d = similarity_matrix.reshape(user_num*curation_num)
print("max : {}".format(similarity_matrix_1d.max()))
# print(similarity_matrix_1d)
plt.plot(similarity_matrix, '.')
plt.axis([0, 9, 0.4, 1])
plt.show()
# print(similarity_matrix)