# from sailer.login import StandardLogin
from sailer.login import StandardLogin, BaseLogin
from sailer.sailer import Sailer
from sailer.locker import *
from sailer.pacific import store_notice_article

class GlsSailer(Sailer):
    login_url = "https://m.skku.edu/skku/main/menu/gls/"
    student_info_url = "http://m.skku.edu/skku/gls/cgereg/cgeregInfoEnq/"
    grade_url = 'https://m.skku.edu/skku/gls/rec/mjrRec/'
    id = b'\x01\x02\x02\x00x\xf8#\xb3ET\x17\x94:\xe8yw\x88#\xc4T\x86\xd0\xac\x8d\xf1n+\x94\x10 \xa0\xaaNV^\x00\x07\x01\x8b=hV:#&\xe1\x86\xe0`;\'\x82M\x80\x00\x00\x00e0c\x06\t*\x86H\x86\xf7\r\x01\x07\x06\xa0V0T\x02\x01\x000O\x06\t*\x86H\x86\xf7\r\x01\x07\x010\x1e\x06\t`\x86H\x01e\x03\x04\x01.0\x11\x04\x0c\x1a\x06\xc6z\xc7\x01\x0f=aX\xd9\x1b\x02\x01\x10\x80"n9\x1b\xd9wF\x86K\xdb\x81\xce\xec)V:t\x19\x1d\xb8\x07\xdbux\xf6^\x10`J\x9b\xbf\xf4\xcd\x0b['
    pw = b'\x01\x02\x02\x00x\xf8#\xb3ET\x17\x94:\xe8yw\x88#\xc4T\x86\xd0\xac\x8d\xf1n+\x94\x10 \xa0\xaaNV^\x00\x07\x01\xe7\xb7\xcd\x86\x81\xca\xb0hg\xbcw\x04\x11<\xacj\x00\x00\x00f0d\x06\t*\x86H\x86\xf7\r\x01\x07\x06\xa0W0U\x02\x01\x000P\x06\t*\x86H\x86\xf7\r\x01\x07\x010\x1e\x06\t`\x86H\x01e\x03\x04\x01.0\x11\x04\x0c\'z\xd6\xba\xf6NB\xf6\x82\x99\xf5\x07\x02\x01\x10\x80#\x1c\x06\xc5r\xa3\xe0$\x15fLe~\x0f\x13w\x9a,R{\xbdE"\x8f\xdc\xe8\x15Ql\xf6%\xc2\x92\x95L\xa6'

    def start(self):
        self.go(self.login_url)
        # tmp = self.css('#username')
        # print(tmp)
        login = BaseLogin(id_element=self.css('#username'),
                              password_element=self.css('#password'),
                              login_element=self.css('#btnLogin > button'))
        login.set_account(id=decrypt(self.id), password=decrypt(self.pw))
        login.do_login()

        self.after_login()

    def after_login(self):
        print('[GLS] Attempt to login')
        if 'j_username' in self.html:
            print('[GLS] Fail to login')
        else:
            print('[GLS] Success to login')
            # self.log(self.html)
            self.student_info_parse()

    def student_info_parse(self):
        self.go(self.student_info_url)
        print("[GLS] Start to parse")

        self.hakbun = self.css("#hakbun").text  #학번
        self.name = self.css('#kor_name').text  #이름
        self.gukjuk = self.css("#gukjuk_cd").text  #국적
        self.jumin = self.css("#jumin_no").text[0:6]  #주민번호
        self.hakwigwajung = self.css("#hakwigwajung_gb").text  #학위과정
        self.jojik = self.css("#jojik_cd").text  #조직
        self.jaehak = self.css("#jaehak_yn").text  #재학
        self.jolupdaesang = self.css("#jolupdaesang_gb").text  #졸업대상
        self.jogijolup = self.css("#jogijolup_yn").text  #조기졸업

        self.chogwadeungrok = self.css("#chogwadeungrok_yn").text  #최과등록
        self.ilbanhyuhak = self.css("#ilbanhyuhak_cnt").text  #일반휴학
        self.dajungong = self.css("#dajungong_gb").text  #다전공

        self.deungrok = self.css("#deungrok_term_cnt").text  #등록학기
        self.ilbanhyuhakterm_cnt = self.css("#ilbanhyuhakterm_cnt").text  #일반휴학 학기
        self.haksuk_yungye_yn = self.css("#haksuk_yungye_yn").text  #학석연계

        print((self.name + self.hakbun + self.gukjuk + self.jumin).split(" "))

        self.xpath('/html/body/div[1]/div[2]/div[1]/ul/li[2]/a').click()

        self.xpath(r'//*[@id="cgeregInfoEnqTab2Grid_1"]')
        # self.xpath('//*[@id="cgeregInfoEnqTab2Grid_1"]')

        self.majors = []
        major = self.xpaths(r'//*[starts-with(@id,"cgeregInfoEnqTab2Grid_")]')
        for m in major:
            self.majors.append(m.text)

        print("[GLS] Finish to crawl student info")
        self.grade_parse()

    def grade_parse(self):
        self.go(self.grade_url)
        self.grades = []
        grade = self.xpaths(r'//*[starts-with(@id,"mjrRecEnqGrid_")]')
        for g in grade:
            self.grades.append(g.text)
        print(len(self.grades))
        print(self.grades)

    def save(self):
        store_notice_article(subject="정국영씨",
                             content="경곱니다",
                             hit="123",
                             writer="위지가",
                             url="최선은아닙니다",
                             created_at="1111-11-11",
                             modified_at="ㅎㅎ")
        print("[GLS] Bye world")

ts = GlsSailer()
ts.start()
ts.save()