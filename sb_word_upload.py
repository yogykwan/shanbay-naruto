# -*- coding: utf-8 -*-
# -*- Python: 2.7.9 -*-

__author__="yogy"
__date__="2015-1-3"

import urllib
import urllib2
import cookielib
import re
import os
import sys
import time
import socket
import threading


homepage="http://www.shanbay.com"

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
    for index,cookie in enumerate(cj):
        print '[',index, ']';
        print cookie.name;
        print cookie.value;
        print '------------';

def initcj():
    cj=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPHandler,urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    opener.open(homepage)
    for index,cookie in enumerate(cj):
        if cookie.name=='csrftoken':
            cjvalue=cookie.value
    postDict={
        'csrfmiddlewaretoken':cjvalue,
        'username':'yogykwan',
        'password':'yogykwan',
    }
    params=urllib.urlencode(postDict)
    loginurl='http://www.shanbay.com/accounts/login/'
    req=urllib2.Request(url=loginurl,data=params,headers=headers)
    resp=opener.open(req)
    return opener,cj

def addlist(opener,listname,bookid):
    postDict={
        'name':listname,
        'description':' ', 
        'wordbook_id':bookid,
    }
    params=urllib.urlencode(postDict)
    addlisturl='http://www.shanbay.com/api/v1/wordbook/wordlist/'
    req=urllib2.Request(url=addlisturl,data=params,headers=headers)
    resp=opener.open(req)

def addword(opener,listid,word):
    postDict={
        'id':listid,
        'word':word,
    }
    params=urllib.urlencode(postDict)
    addwordurl='http://www.shanbay.com/api/v1/wordlist/vocabulary/'
    req=urllib2.Request(url=addwordurl,data=params,headers=headers)
    try:
        resp=opener.open(req,timeout=10)
    except Exception as e:
        print 'Error is: '+str(e)+' | '+word+' | '+listid
        time.sleep(1)
        addword(opener,listid,word)

def addwords(opener,listurl,listname):
    listfile=open(listname,'r')
    words=listfile.read().replace('&#39;','\'').split(',')
    for i in words:
        addword(opener,listurl,i)
    listfile.close()
    
def addbook(opener,bookid):
    bookurl='http://www.shanbay.com/wordbook/'+bookid
    bookpage=urllib2.urlopen(bookurl).read()
    pattern=re.compile(b'<a href="/wordlist/'+bookid+'/(.*?)</a>')
    listurls=re.findall(pattern,bookpage)
    flag=0
    cnt=0
    urls=[]
    names=[]
    for i in listurls[300:500]:
        flag=1-flag
        if flag==0: continue
        listurl=i[:6]
        listname=i[9:]
        cnt=cnt+1
        #addwords(opener,listurl,listname)
        urls.append(listurl)
        names.append(listname)
    threads=[]
    for i in range(cnt):
        t=threading.Thread(target=addwords,args=[opener,urls[i],names[i]])
        threads.append(t)
    for i in range(cnt):
        threads[i].start()
    for i in range(cnt):
        threads[i].join()

def movelist(opener,oldbook,newbook,listurl):
    postDict={
        'wordbook_id':oldbook,
        'wordlist_id':listurl,
        'new_wordbook_id':newbook,
    }
    params=urllib.urlencode(postDict)
    movelisturl='http://www.shanbay.com/api/v1/wordbook/wordlist/'
    req=urllib2.Request(url=movelisturl,data=params,headers=headers)
    req.get_method = lambda: 'PUT'
    resp=opener.open(req)
    #print resp.read()

def movebook(opener,oldbook,newbook,lists):
    bookurl='http://www.shanbay.com/wordbook/'+oldbook
    bookpage=urllib2.urlopen(bookurl).read()
    pattern=re.compile(b'<a href="/wordlist/'+oldbook+b'/(.*?)</a>')
    listurls=re.findall(pattern,bookpage)
    flag=0
    d={'0':'0'}
    for i in listurls:
        flag=1-flag
        if flag==0: continue
        listurl=i[:6]
        listname=i[9:]
        d[listname.split(' ')[0]]=listurl
    for i in lists:
        print i,' --> ',d[i.split(' ')[0]]
        movelist(opener,oldbook,newbook,d[i.split(' ')[0]])
        return

if __name__ == '__main__':
    opener,cj=initcj()
    file=open('listnames','r')
    lists=[]
    while 1:
        line=file.readline().strip('\n')
        if not line: break
        lists.append(line)
    #for i in lists: addlist(opener,i,'95326')
    #addbook(opener,'95326')
    movelist(opener,'86803','95338','112687')
    file.close()

    
