"""
labelling: on-hot

1.Belong -> 누구에게 해당되는 글인가
전공: [유학, 문과, 법과, 사회과학, 경제,
      경영, 사범, 예술, 자연과학, 정보통신, 소프트웨어,
       공과, 약학, 생명공학, 스포츠과학, 의과, 융합]   0~16
학년: [1학기, 2학기, 3학기, 4학기, 5학기, 6학기, 7학기, 8학기, 초과학기] 17~25
기타: [재학, 휴학, 남자, 여자] 26~29
=> [전공, 학년, 재학] / 17+9+4 = 30개

2.Property -> 이 글이 어떤 속성을 가지고 있는가
[장학금, 대외활동, 대학원, 취업, 인턴, 학사일정, 특강, 교환학생, 기타] 9
"""
import numpy as np
import json
from collections import OrderedDict


majors = ["scos.skku", "liberalarts.skku", "law.skku", "sscience.skku", "ecostat.skku",
          "biz.skku", "coe.skku", "art.skku", "cscience.skku", "icc.skku", "cs.skku",
          "shb.skku", "pharm.skku", "biotech.skku", "sport.skku", "skkumed.skku", "icon.skku"]

# json file path
belong_json_file = '../content_belong_label_keyword'
property_json_file = '../content_property_label_keyword'

# json data
belong_json_data = open(belong_json_file).read()
property_json_data = open(property_json_file).read()

# dictionary data
belong_dict = json.loads(belong_json_data)
property_dict = json.loads(property_json_data)
belong_dict = OrderedDict(sorted(belong_dict.items(), key=lambda t: t[0]))
property_dict = OrderedDict(sorted(property_dict.items(), key=lambda t: t[0]))
# print(belong_dict)
print(tuple(belong_dict.keys()))
print(tuple(property_dict.keys()))

# print(len(belong_label))

fr = open('../data.txt', 'r')
fbw = open('../data_belong_label.txt', 'w')
fpw = open('../data_property_label.txt', 'w')

lines = fr.readlines()

'''Belong'''
for line in lines:
    belong_label = np.zeros(len(belong_dict), dtype=np.uint8)
    property_label = np.zeros(len(property_dict), dtype=np.uint8)
    for i, values in enumerate(belong_dict.values()):
        for value in values:
            if value in line:
                belong_label[i] = 1
    for j, values in enumerate(property_dict.values()):
        for value in values:
            if value in line:
                property_label[j] = 1
    fbw.write(' '.join(str(i) for i in belong_label))
    fbw.write('\n')
    fpw.write(' '.join(str(i) for i in property_label))
    fpw.write('\n')

fr.close()
fbw.close()
fpw.close()



'''Property'''


# fr = open('../data.txt', 'r')
# fbw = open('../data_belong_label.txt', 'w')
# fpw = open('../data_property_label.txt', 'w')
#
# # lists = [1, 2, 3]
# # fw.write(" ".join(str(i) for i in lists))
#
# lines = fr.readlines()
# print(len(lines))
# for line in lines:
#     label_belong = np.zeros(29, dtype=np.uint8)
#     label_property = np.zeros(9, dtype=np.uint8)
#
#     url = line.split(" ")[0]
#
#
#     fbw.write(' '.join(str(i) for i in label_belong))
#     fbw.write('\n')
#     fpw.write(' '.join(str(i) for i in label_property))
#     fpw.write('\n')
#
# fr.close()
# fbw.close()
# fpw.close()
