"""
labelling: on-hot

1.Belong -> 누구에게 해당되는 글인가
전공: [유학, 문과, 법과, 사회과학, 경제,
      경영, 사범, 예술, 자연과학, 정보통신, 소프트웨어,
       공과, 약학, 생명공학, 스포츠과학, 의과, 융합]   0~16
학년: [1학기, 2학기, 3학기, 4학기, 5학기, 6학기, 7학기, 8학기, 초과학기] 17~25
재학: [재학, 휴학, 졸업예정] 26~28
=> [전공, 학년, 재학] / 17+9+3 = 29개

2.Property -> 이 글이 어떤 속성을 가지고 있는가
[장학금, 대외활동, 대학원, 취업, 인턴, 학사일정, 특강, 교환학생, 기타] 9
"""
import numpy as np


'''Belong'''


def labelling_major(url, str, arr):
    # [1] url 링크로 소속 전공 판별
    for i, major in enumerate(majors, 0):
        if major in url:
            arr[i] = 1
            break

    # [2] 글 내용으로 판별


def labelling_semester(str, arr):
    if ("hakbu.skku" or "1학년" or "신입생" or "새내기" or
        "전공진입" or "전공 진입") in str:
        arr[17] = 1
        arr[18] = 1

    if ("2학년" or "3학기" or "4학기") in str:
        arr[19] = 1
        arr[20] = 1

    if ("3학년" or "5학기" or "6학기") in str:
        arr[21] = 1
        arr[22] = 1

    if ("졸업" or "4학년" or "7학기" or "8학기") in str:
        arr[23] = 1
        arr[24] = 1

    if ("초과 학기" or "초과학기" or "졸업유예" or "졸업 유예" or "수료") in str:
        arr[25] = 1


def labelling_attend(str, arr):
    if "졸업" in str:
        arr[26] = 1
        arr[28] = 1
    pass


majors = ["scos.skku", "liberalarts.skku", "law.skku", "sscience.skku", "ecostat.skku",
          "biz.skku", "coe.skku", "art.skku", "cscience.skku", "icc.skku", "cs.skku",
          "shb.skku", "pharm.skku", "biotech.skku", "sport.skku", "skkumed.skku", "icon.skku"]


'''Property'''


def labeling_scholarship(str, arr):
    if ("장학" or "재단" or "대출" or "학자금") in str:
        arr[0] = 1


def labelling_contest(str, arr):
    if ("대회" or "캠프" or "경진" or "창업" or "페스티벌" or "아이디어" or "봉사" or "참가" or "공모" or "대외활동") in str:
        arr[1] = 1


def labelling_graduated(str, arr):
    if ("대학원" or "석사" or "박사" or "석박" or "학석") in str:
        arr[2] = 1


def labelling_job(str, arr):
    if ("취업" or "채용" or "공채" or "특채" or "경력") in str:
        arr[3] = 1


def labelling_intern(str, arr):
    if ("채용형" or "인턴" or "intern") in str:
        arr[4] = 1


def labelling_schedule(str, arr):
    if ("신청" or "일정" or "복학" or "기간" or "강의평가" or "기한" or "학사" or "수강") in str:
        arr[5] = 1


def labelling_lecture(str, arr):
    if ("특강" or "설명회" or "세미나" or "콜로키움" or "발표" or "박람회") in str:
        arr[6] = 1


def labelling_exchange(str, arr):
    if ("교환학생" or "수학생" or "파견" or "유학") in str:
        arr[7] = 1


def labelling_etc(arr):
    for item in arr:
        if item == 1:
            return
    arr[8] = 1


fr = open('data.txt', 'r')
fbw = open('data_belong_label.txt', 'w')
fpw = open('data_property_label.txt', 'w')

# lists = [1, 2, 3]
# fw.write(" ".join(str(i) for i in lists))

lines = fr.readlines()
print(len(lines))
for line in lines:
    label_belong = np.zeros(29, dtype=np.uint8)
    label_property = np.zeros(9, dtype=np.uint8)

    url = line.split(" ")[0]

    labelling_major(url, line, label_belong)
    labelling_semester(line, label_belong)
    labelling_attend(line, label_belong)

    labeling_scholarship(line, label_property)
    labelling_contest(line, label_property)
    labelling_graduated(line, label_property)
    labelling_job(line, label_property)
    labelling_intern(line, label_property)
    labelling_schedule(line, label_property)
    labelling_lecture(line, label_property)
    labelling_etc(label_property)

    fbw.write(' '.join(str(i) for i in label_belong))
    fbw.write('\n')
    fpw.write(' '.join(str(i) for i in label_property))
    fpw.write('\n')

fr.close()
fbw.close()
fpw.close()
