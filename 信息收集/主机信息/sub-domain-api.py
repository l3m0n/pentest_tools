#!/usr/bin/env python
# encoding: utf-8
 
import re
import sys
import json
import time
import socket
import random
import urllib
import urllib2
 
from bs4 import BeautifulSoup
 
# 随机AGENT
USER_AGENTS = [
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
]
 
 
def random_useragent():
    return random.choice(USER_AGENTS)
 
def getUrlRespHtml(url):
    respHtml=''
    try:
        heads = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
                'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
                'Accept-Language':'zh-cn,zh;q=0.5', 
                'Cache-Control':'max-age=0', 
                'Connection':'keep-alive', 
                'Keep-Alive':'115',
                'User-Agent':random_useragent()}
      
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        urllib2.install_opener(opener) 
        req = urllib2.Request(url)
        opener.addheaders = heads.items()
        respHtml = opener.open(req).read()
    except Exception:
        pass
    return respHtml
 
def links_get(domain):
    trytime = 0
    #links里面得到的数据不是很全，准确率没法保证
    domainslinks = []
    try:
        req=urllib2.Request('http://i.links.cn/subdomain/?b2=1&b3=1&b4=1&domain='+domain)
        req.add_header('User-Agent',random_useragent())
        res=urllib2.urlopen(req, timeout = 30)
        src=res.read()
 
        TempD = re.findall('value="http.*?">',src,re.S)
        for item in TempD:
            item = item[item.find('//')+2:-2]
            #result=socket.getaddrinfo(item,None)
            #print result[0][4]
            domainslinks.append(item)
            domainslinks={}.fromkeys(domainslinks).keys()
        return domainslinks
 
    except Exception, e:
        pass
        trytime += 1
        if trytime > 3:
            return domainslinks
 
def bing_get(domain):
    trytime = 0
    f = 1
    domainsbing = []
    #bing里面获取的数据不是很完全
    while True:
        try:            
            req=urllib2.Request('http://cn.bing.com/search?count=50&q=site:'+domain+'&first='+str(f))
            req.add_header('User-Agent',random_useragent()) 
            res=urllib2.urlopen(req, timeout = 30)
            src=res.read()
            TempD=re.findall('<cite>(.*?)<\/cite>',src)
            for item in TempD:
                item=item.split('<strong>')[0]
                item += domain
                try:
                    if not (item.startswith('http://') or item.startswith('https://')):
                        item = "http://" + item
                    proto, rest = urllib2.splittype(item)
                    host, rest = urllib2.splithost(rest) 
                    host, port = urllib2.splitport(host)
                    if port == None:
                        item = host
                    else:
                        item = host + ":" + port
                except:
                     print traceback.format_exc()
                     pass                          
                domainsbing.append(item)         
            if f<500 and re.search('class="sb_pagN"',src) is not None:
                f = int(f)+50
            else:
                subdomainbing={}.fromkeys(domainsbing).keys()
                return subdomainbing
                break
        except Exception, e:
            pass
            trytime+=1
            if trytime>3:
                return domainsbing
 
def google_get(domain):
    trytime = 0
    s=1
    domainsgoogle=[]
    #需要绑定google的hosts
    while True:
        try:
            req=urllib2.Request('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=site:'+domain+'&rsz=8&start='+str(s))
            req.add_header('User-Agent',random_useragent()) 
            res=urllib2.urlopen(req, timeout = 30)
            src=res.read()
            results = json.loads(src)
            TempD = results['responseData']['results']
            for item in TempD:
                item=item['visibleUrl'] 
                item=item.encode('utf-8')
                domainsgoogle.append(item)                
            s = int(s)+8
        except Exception, e:
            trytime += 1
            if trytime >= 3:
                domainsgoogle={}.fromkeys(domainsgoogle).keys()
                return domainsgoogle 
 
def Baidu_get(domain):
    domainsbaidu=[]
    try:
        pg = 10
        for x in xrange(1,pg):
            rn=50
            pn=(x-1)*rn
            url = 'http://www.baidu.com/baidu?cl=3&tn=baidutop10&wd=site:'+domain.strip()+'&rn='+str(rn)+'&pn='+str(pn)
            src=getUrlRespHtml(url)
            soup = BeautifulSoup(src)
            html=soup.find('div', id="content_left")
            if html:
                html_doc=html.find_all('h3',class_="t")
                if html_doc:
                    for doc in html_doc:
                        href=doc.find('a')
                        link=href.get('href')
                        #需要第二次请求,从302里面获取到跳转的地址[速度很慢]
                        rurl=urllib.unquote(urllib2.urlopen(link.strip()).geturl()).strip()
                        reg='http:\/\/[^\.]+'+'.'+domain
                        match_url = re.search(reg,rurl)
                        if match_url:
                            item=match_url.group(0).replace('http://','')
                            domainsbaidu.append(item)
    except Exception, e:
        pass
        domainsbaidu={}.fromkeys(domainsbaidu).keys()
 
    return domainsbaidu
 
def get_360(domain):
    #从360获取的数据一般都是网站管理员自己添加的，所以准备率比较高。
    domains360=[]
    try:
        url = 'http://webscan.360.cn/sub/index/?url='+domain.strip()
        src=getUrlRespHtml(url)
        item = re.findall(r'\)">(.*?)</strong>',src)
        if len(item)>0:
            for i in xrange(1,len(item)):
                domains360.append(item[i])
        else:
            item = ''
            domains360.append(item)
    except Exception, e:
        pass
        domains360={}.fromkeys(domains360).keys()
    return domains360
 
def get_subdomain_run(domain):
    mydomains = []
    mydomains.extend(links_get(domain))
    mydomains.extend(bing_get(domain))
    mydomains.extend(Baidu_get(domain))
    mydomains.extend(google_get(domain))
    mydomains.extend(get_360(domain))
    mydomains = list(set(mydomains))
 
    return mydomains
 
if __name__ == "__main__":
   if len(sys.argv) == 2:
      print get_subdomain_run(sys.argv[1])
      sys.exit(0)
   else:
       print ("usage: %s domain" % sys.argv[0])
       sys.exit(-1)