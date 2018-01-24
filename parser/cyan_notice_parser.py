import json

from sailer.locker import decrypt
from sailer.login import BaseLogin
from sailer.sailer import Sailer
from sailer.pacific import store_notice_article
from sailer.utils import convert_datetime
import time

class CyanNoticeSailer(Sailer):
    login_url = "https://m.skku.edu/skku/main/menu/gls/"
    notice_url = "https://m.skku.edu/skku/kingo/kingoNotice/"
    id = b'\x01\x02\x02\x00x\xf8#\xb3ET\x17\x94:\xe8yw\x88#\xc4T\x86\xd0\xac\x8d\xf1n+\x94\x10 \xa0\xaaNV^\x00\x07\x01\x8b=hV:#&\xe1\x86\xe0`;\'\x82M\x80\x00\x00\x00e0c\x06\t*\x86H\x86\xf7\r\x01\x07\x06\xa0V0T\x02\x01\x000O\x06\t*\x86H\x86\xf7\r\x01\x07\x010\x1e\x06\t`\x86H\x01e\x03\x04\x01.0\x11\x04\x0c\x1a\x06\xc6z\xc7\x01\x0f=aX\xd9\x1b\x02\x01\x10\x80"n9\x1b\xd9wF\x86K\xdb\x81\xce\xec)V:t\x19\x1d\xb8\x07\xdbux\xf6^\x10`J\x9b\xbf\xf4\xcd\x0b['
    pw = b'\x01\x02\x02\x00x\xf8#\xb3ET\x17\x94:\xe8yw\x88#\xc4T\x86\xd0\xac\x8d\xf1n+\x94\x10 \xa0\xaaNV^\x00\x07\x01\xe7\xb7\xcd\x86\x81\xca\xb0hg\xbcw\x04\x11<\xacj\x00\x00\x00f0d\x06\t*\x86H\x86\xf7\r\x01\x07\x06\xa0W0U\x02\x01\x000P\x06\t*\x86H\x86\xf7\r\x01\x07\x010\x1e\x06\t`\x86H\x01e\x03\x04\x01.0\x11\x04\x0c\'z\xd6\xba\xf6NB\xf6\x82\x99\xf5\x07\x02\x01\x10\x80#\x1c\x06\xc5r\xa3\xe0$\x15fLe~\x0f\x13w\x9a,R{\xbdE"\x8f\xdc\xe8\x15Ql\xf6%\xc2\x92\x95L\xa6'
    urls = []
    pages = 1

    def start(self):
        print("[GLS] Start to parse gls notice")
        self.go(self.login_url)
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
            self.cyan_notice_link_parse()

    def cyan_notice_link_parse(self):
        self.go(self.notice_url)
        i = 1
        while i <= self.pages:
            # for j in range(1, 11):
            #     link = self.xpath(r'//*[@id="noticeList_{}"]/td[1]/a'.format(j)).get_attribute('href')
            #     self.urls.append(link)
            links = self.xpaths(r'//*[starts-with(@id,"noticeList_")]/td[1]/a')
            for link in links:
                self.urls.append(link.get_attribute('href'))

            i = i + 1
            if i <= 6:
                self.xpath('//*[@id="noticeList"]/div/button[{}]'.format(i)).click()
            else:
                self.xpath('//*[@id="noticeList"]/div/button[{}]'.format((i - 7) % 5 + 4)).click()
            print("[SLEEP {}]".format(i - 1), end=" ")
            time.sleep(1)
            print("[AWAKE]")

        self.cyan_notice_parse()

    def cyan_notice_parse(self):
        print(len(self.urls))
        for url in self.urls:
            self.go(url)

            subject = self.xpath(r'//*[@id="ct"]/div[1]/h2').text
            writer = " ".join([x.strip() for x in self.xpath(r'//*[@id="ct"]/div[1]/p').text.split('|')[0:2]])
            content = self.xpath(r'//*[@id="ct"]/div[2]').text
            date = self.xpath(r'//*[@id="ct"]/div[1]/p').text.split('|')[2].strip()

            create_at = convert_datetime(date, '%Y/%m/%d')
            # print(url)
            # print(create_at)
            res = store_notice_article(subject=subject,
                                 content=content,
                                 writer=writer,
                                 url=url,
                                 created_at=create_at)

            if res["result"] == "failed":
                if res["error"] == "already existed item":
                    print("[GLS] All notice is up to date")
                    return
        print("[GLS] Success parse {} gls notice".format(len(self.urls)))



ns = CyanNoticeSailer()
ns.start()

