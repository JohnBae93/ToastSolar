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
import re

import numpy as np
import json
from collections import OrderedDict

"""
SETTING
"""
majors = ["scos.skku", "liberalarts.skku", "law.skku", "sscience.skku", "ecostat.skku",
          "biz.skku", "coe.skku", "art.skku", "cscience.skku", "icc.skku", "cs.skku",
          "shb.skku", "pharm.skku", "biotech.skku", "sport.skku", "skkumed.skku", "icon.skku"]

# json file path
belong_json_file = '../content_belong_label_keyword.json'
property_json_file = '../content_property_label_keyword.json'


def load_data(filename):
    file_content = open(filename).read()
    data_list = json.loads(file_content)
    data_list.sort(key=lambda x: x["label"])
    return data_list


def check_keywords(data, line):
    try:
        diff_mode = data["keywords"]["type"]
    except Exception as e:
        print(data)
        raise Exception("Cannot read keyword type at data {}".format(data))

    p_match_word = re.compile(r"[가-힣A-Za-z0-9]")

    for keyword in data["keywords"]["list"]:
        if diff_mode == "EXACT":
            return keyword in line
        elif diff_mode == "INCLUDE_LETTER":
            new_line = "".join(p_match_word.findall(line))
            new_keyword = "".join(p_match_word.findall(keyword))
            return new_keyword in new_line

    return False


# dictionary data
belong_data = load_data(belong_json_file)
property_data = load_data(property_json_file)

# print(belong_dict)
print(tuple(belong_data))
print(tuple(property_data))

# print(len(belong_label))
input_file = open('../data.txt', 'r')
belong_file = open('../data_belong_label.txt', 'w')
property_file = open('../data_property_label.txt', 'w')

lines = input_file.readlines()

'''Belong'''
for line in lines:
    belong_label = np.zeros(len(belong_data), dtype=np.uint8)
    property_label = np.zeros(len(property_data), dtype=np.uint8)

    for i, data in enumerate(belong_data):
        if check_keywords(data, line):
            belong_label[i] = 1

    for i, data in enumerate(property_data):
        if check_keywords(data, line):
            property_label[i] = 1

    belong_file.write(' '.join(str(i) for i in belong_label))
    belong_file.write('\n')
    property_file.write(' '.join(str(i) for i in property_label))
    property_file.write('\n')

input_file.close()
belong_file.close()
property_file.close()



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



"""
Convert

from : /"([^"]+)":..\s+((("[^"]+"),?\s*)+)/g
to : {"label":"$1", \n "keywords": {\n  "type":"EXACT",\n  "list": [$2]}},\n
"""