import numpy as np

major_urls = ["scos.skku", "liberalarts.skku", "law.skku", "sscience.skku", "ecostat.skku",
              "biz.skku", "coe.skku", "art.skku", "cscience.skku", "icc.skku", "cs.skku",
              "shb.skku", "pharm.skku", "biotech.skku", "sport.skku", "skkumed.skku", "icon.skku"]

major_names = ['유학', '문과', '법과', '사회과학', '경제', '경영', '사범', '예술', '자연과학', '정보통신', '소프트웨어', '공과', '약학', '생명공학', '스포츠과학',
               '의과', '융합']


def pearson_similarity(vector1, vector2):
    return np.corrcoef(vector1, vector2)[0][1]


def if_letters_in_content(letters, content):
    if any(s in content for s in letters):
        return True
    return False


class Curation:
    def __init__(self, _content):
        self.belong_label = np.zeros(29, dtype=np.float32)
        self.property_label = np.zeros(9, dtype=np.float32)
        self.content = _content
        self.url = _content.split(" ")[0]

        self.labelling_major()
        self.labelling_semester()
        self.labelling_attend()

        self.labeling_scholarship()
        self.labelling_contest()
        self.labelling_graduated()
        self.labelling_job()
        self.labelling_intern()
        self.labelling_schedule()
        self.labelling_lecture()
        self.labelling_etc()

    def labelling_major(self):
        # [1] url 링크로 소속 전공 판별
        for i, major in enumerate(major_urls, 0):
            if major in self.url:
                self.belong_label[i] = 1
                break

        # [2] 글 내용으로 판별

    def labelling_semester(self):
        letters = ("hakbu.skku", "1학년", "신입생", "새내기", "전공진입", "전공 진입")
        if if_letters_in_content(letters, self.content):
            self.belong_label[17] = 1
            self.belong_label[18] = 1

        letters = ("2학년", "3학기", "4학기")
        if if_letters_in_content(letters, self.content):
            self.belong_label[19] = 1
            self.belong_label[20] = 1

        letters = ("3학년", "5학기", "6학기", "편입")
        if if_letters_in_content(letters, self.content):
            self.belong_label[21] = 1
            self.belong_label[22] = 1

        letters = ("졸업", "4학년", "7학기", "8학기")
        if if_letters_in_content(letters, self.content):
            self.belong_label[23] = 1
            self.belong_label[24] = 1

        letters = ("초과 학기", "초과학기", "졸업유예", "졸업 유예", "수료")
        if if_letters_in_content(letters, self.content):
            self.belong_label[25] = 1

    def labelling_attend(self):
        if "졸업" in self.content:
            self.belong_label[26] = 1
            self.belong_label[28] = 1
        elif "복학" in self.content:
            self.belong_label[27] = 1
        else:
            pass

    def labeling_scholarship(self):
        letters = ("장학", "재단", "대출", "학자금")
        if if_letters_in_content(letters, self.content):
            self.property_label[0] = 1

    def labelling_contest(self):
        letters = ("대회", "캠프", "경진", "창업", "페스티벌", "아이디어", "봉사", "참가", "공모", "대외활동")
        if if_letters_in_content(letters, self.content):
            self.property_label[1] = 1

    def labelling_graduated(self):
        letters = ("대학원", "석사", "박사", "석박", "학석")
        if if_letters_in_content(letters, self.content):
            self.property_label[2] = 1

    def labelling_job(self):
        letters = ("취업", "채용", "공채", "특채", "경력")
        if if_letters_in_content(letters, self.content):
            self.property_label[3] = 1

    def labelling_intern(self):
        letters = ("채용형", "인턴", "intern")
        if if_letters_in_content(letters, self.content):
            self.property_label[4] = 1

    def labelling_schedule(self):
        letters = ("신청", "일정", "복학", "기간", "강의평가", "기한", "학사", "수강신청", "졸업")
        if if_letters_in_content(letters, self.content):
            self.property_label[5] = 1

    def labelling_lecture(self):
        letters = ("특강", "설명회", "세미나", "콜로키움", "발표", "박람회")
        if if_letters_in_content(letters, self.content):
            self.property_label[6] = 1

    def labelling_exchangeself(self):
        letters = ("교환학생", "수학생", "파견", "유학")
        if if_letters_in_content(letters, self.content):
            self.property_label[7] = 1

    def labelling_etc(self):
        for item in self.property_label:
            if item == 1:
                return
        self.property_label[8] = 1


class User:
    def __init__(self, _majors, _semester, _attend):
        self.belong_label = np.zeros(29, dtype=np.float32)
        self.property_label = np.zeros(9, dtype=np.float32)

        self.majors = _majors
        self.semester = _semester
        self.attend = _attend

        self.labelling_major()
        self.labelling_semester()
        self.labelling_attend()

    def labelling_major(self):
        for major in self.majors:
            for name in major_names:
                if name in major:
                    self.belong_label[major_names.index(name)] = 1

    def labelling_semester(self):
        if self.semester <= 8 and self.semester >= 1:
            self.belong_label[int(self.semester) + 16] = 1
        else:
            self.belong_label[25] = 1

    def labelling_attend(self):
        if self.attend == '예':
            self.belong_label[26] = 1
        elif self.attend == '아니오':
            self.belong_label[27] = 1

        if self.semester >= 7:
            self.belong_label[28] = 1

majors = ['정보통신대학-', '소프트웨어대학-']
label=np.zeros(29, dtype=np.uint8)
for major in majors:
    for name in major_names:
        if name in major:
            label[major_names.index(name)] = 1

fr = open('data.txt', 'r', encoding='utf-8')
lines = fr.readlines()
curations = []
for line in lines:
    curation = Curation(line)
    curations.append(curation)

print(lines[2])
np.set_printoptions(threshold=np.nan)
print(curations[2].belong_label)
print(curations[2].property_label)