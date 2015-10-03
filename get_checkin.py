# -*- coding: utf-8 -*-
# -*- Python: 2.7.3 -*-

__author__="yogy"
__date__="2015-10-03"

import urllib
import urllib2
import cookielib
import re
import zlib
import chardet

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


def printCJ(cj):
    for index, cookie in enumerate(cj):
        print '[', index, ']',
        print cookie.name,
        print cookie.value,
        print '------------'


def initCJ():
    loginUrl='http://www.shanbay.com/accounts/login/'
    cj=cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPHandler, urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    opener.open(loginUrl)
    for index, cookie in enumerate(cj):
        if cookie.name == 'csrftoken':
            cjvalue = cookie.value
    postDict = {
        'csrfmiddlewaretoken': cjvalue,
        'username': 'yogy_test', //replace yogy_test by your username
        'password': 'kwan_test', //replace kwan_test by your password
        'token': '',
        'token': '',
    }
    params = urllib.urlencode(postDict)
    req = urllib2.Request(url=loginUrl, data=params, headers=headers)
    resp = opener.open(req)
    #printCJ(cj)
    return opener, cj


def getData(opener):
    myFile = open("record1.txt", "w")
    tot = 1000
    for i in range(1, 1000):
        if i > tot: break
        page = "http://www.shanbay.com/checkin/user/8840443/?page="+str(i) //replace 8840443 by your userid 
        req = urllib2.Request(url=page, headers=headers)
        resp = opener.open(req)
        content = resp.read()
        gzipped = resp.headers.get('Content-Encoding')
        if gzipped: html = zlib.decompress(content, 16+zlib.MAX_WBITS)
        else: html = content
        result = chardet.detect(html)
        # print result
        if tot == 1000:
            tmp = re.findall(re.compile(b'" rel="page">(.*?)</a>'), html)
            tot = int(tmp[-2])
        num = re.findall(re.compile(b'<span class="number"> (.*?) </span>'), html)
        note = re.findall(re.compile(b'<div class="note">((.|\n)*?)</div>'), html)
        date = re.findall(re.compile(b'class="target">(.*?)</a>'), html)
        for i in range(len(note)):
            note[i]=note[i][0].replace('\n','').replace(' ','')
            print num[i], note[i], date[i]
            line1 = "♫Yogy第"+num[i]+"天打卡日记：" //replace ♫Yogy by your nickname
            line2 = note[i]
            line3 = date[i]
            myFile.write(line1+"\n")
            myFile.write(line2+"\n")
            myFile.write(line3+"\n")
            myFile.write("\n---\n")

if __name__ == '__main__':
    opener, cj = initCJ()
    getData(opener)
