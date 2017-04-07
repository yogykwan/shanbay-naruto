# -*- coding: utf-8 -*-
# -*- Python: 2.7.3 -*-

__author__="yogy"
__date__="2015-3-15"

import urllib
import urllib2
import cookielib
import re
import xlrd
from xlwt import *
import datetime

homepage="http://www.shanbay.com"
loginurl='http://www.shanbay.com/accounts/login/'
global line

headers={
    'User-Agent':r'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36',
    'Connection':r'keep-alive',
    'Origin':r'http://www.shanbay.com',
    'Host':r'www.shanbay.com',
    'X-Requested-With':r'XMLHttpRequest',
    'Content-Type':r'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept':r'*/*',
    'Accept-Encoding':r'gzip,deflate,sdch',
    'Accept-Language':r'zh-CN,zh;q=0.8',
    'Referer':r'http://www.shanbay.com/',
}

def printcj(cj):
    print "print cj:"
    for index,cookie in enumerate(cj):
        print '[',index, ']';
        print cookie.name;
        print cookie.value;
        print '------------';

def initcj():
    cj=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPHandler,urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    opener.open(loginurl)
    for index,cookie in enumerate(cj):
        if cookie.name=='csrftoken':
            cjvalue=cookie.value
    postDict={
        'csrfmiddlewaretoken':cjvalue,
        'username':'_Pikachu_',
        'password':'12345678',
    }
    params=urllib.urlencode(postDict)
    req=urllib2.Request(url=loginurl,data=params,headers=headers)
    resp=opener.open(req)
    return opener,cj


def getpage(url,num,ws,pm):
    global line
    pageurl=url+str(num)
    pagedata=urllib2.urlopen(pageurl).read()
    #pattern=re.compile(b'<p>(.*?)</p>')
    pattern=[]
    pattern.append(re.compile(b'<p>'+pm+'(.*?)</p>'))
    pattern.append(re.compile(b'<p>成员数(.*?)</p>'))
    pattern.append(re.compile(b'<p>打卡率(.*?)</p>'))
    pattern.append(re.compile(b'<p>总成长值(.*?)</p>'))
    data=[]
    for i in range(4):
        data.append(re.findall(pattern[i],pagedata))
    cnt=len(data[0])
    print num,cnt
    for i in range(cnt):
        for j in range(4):
            data[j][i]=data[j][i].strip()
            if data[j][i][0]=='[':
                data[j][i]=data[j][i][14:]
            if data[j][i][0].isdigit()==False:
                #print data[j][i]
                data[j][i]=data[j][i][3:]
            if data[j][i][0].isdigit()==False:
                if j==3: line=line-1
                continue
            if j==0:
                if len(data[j][i])>4:
                    data[j][i]=data[j][i][:2]
            if j==1:
                if len(data[j][i])>7:
                    data[j][i]=data[j][i][:7]
                if data[j][i][1]=='_':
                    data[j][i]='50/75'
            if j==2:
                for p in range(len(data[j][i])):
                    #print data[j][i][p]
                    if data[j][i][p]=='%':
                        data[j][i]=data[j][i][:p+1]
                        break
            if j==3:
                if len(data[j][i])>5 and data[j][i][5]=='*':
                    data[j][i]=data[j][i][:5]
            print data[j][i],
            ws.write(line,j+1,data[j][i])
        line=line+1
        print ""

if __name__ == '__main__':
    opener,cj=initcj()
    #printcj(cj)
    line=0
    w=Workbook()
    ws = w.add_sheet('sheet1')
    ws.write(85,1,'23')
    ws.write(144,3,'99.45%')
    for i in range(1,12): getpage("http://www.shanbay.com/team/thread/3352/199735/?page=",i,ws,"排名")
    for i in range(1,11): getpage("http://www.shanbay.com/team/thread/3352/259669/?page=",i,ws,"排名")
    for i in range(10,24): getpage("http://www.shanbay.com/team/thread/3352/259669/?page=",i,ws,"周排名")

    cnt=0
    now=datetime.datetime.now()
    oneday = datetime.timedelta(days=-1)
    now=now+oneday
    for i in range(line):
        date=now.strftime('%Y-%m-%d')
        ws.write(line-1-i,0,date)
        now=now+oneday
        cnt=cnt+1
        if cnt==6:
            cnt=0
            now=now+oneday
    ws.col(0).width=256*15
    ws.col(1).width=256*5
    ws.col(2).width=256*15
    ws.col(3).width=256*15
    ws.col(4).width=256*15
    w.save('data.xls')
