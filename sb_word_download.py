# -*- coding: utf-8 -*-
# -*- Python: 2.7.9 -*-

__author__="yogy"
__date__="2015-1-3"

import urllib
import urllib2
import cookielib
import re

homepage="http://www.shanbay.com"

def getlist(listurl,listname):
    listfile=open(listname,'w+')
    pagenum=0
    for i in range(1,100):
        pageurl=listurl+'?page='+str(i)
        listpage=urllib2.urlopen(pageurl).read()
        pattern=re.compile(b'<td class="span2"><strong>(.*?)</strong></td>')
        words=re.findall(pattern,listpage)
        if words:
            pagenum+=1
            for j in words:
                listfile.write(j)
                listfile.write(',')
        else:
            print listname, pagenum
            listfile.close()
            return

def getbook(bookurl):
    bookpage=urllib2.urlopen(bookurl).read()
    pattern=re.compile(b'<a href="/wordlist/80770/(.*?)</a>')
    listurls=re.findall(pattern,bookpage)
    lists=[]
    for i in listurls:
        listurl=homepage+'/wordlist/80770/'+i[:6]
        if listurl[-1]!='/':
            listurl=listurl+'/'
        listname=i[8:]
        if listname[0]=='>':
            listname=listname[1:]
        if(listname.count('  ')): print listname
        listname=listname.replace('  ',' ').replace('&#39;','\'')
        lists.append(listname)
        #getlist(listurl,listname)
    return lists

def weight(s):
    cnt=s.count('.')
    for i in range(5-cnt): s=s+'.'
    ans=0
    for i,j in enumerate(s):
        if j=='.': ans=ans*100
        elif s[i+1]=='.': ans=ans+int(j)
        else: ans=ans+10*int(j)
    return ans
        
def my_cmp(x,y):
    a=x.split(' ')[0]
    b=y.split(' ')[0]
    p=weight(a)
    q=weight(b)
    return cmp(p,q)

if __name__ == '__main__':
    bookurl=homepage+'/wordbook/80770/'
    lists=getbook(bookurl)
    exit(0)
    lists.sort(my_cmp)
    print lists[:50]
    bookfile=open('listnames','w+')
    for i in lists:
        bookfile.write(i)
        bookfile.write('\n')
    bookfile.close()
    
