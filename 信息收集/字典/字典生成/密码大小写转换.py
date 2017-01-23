#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# 密码大小写字母转换
# Usage: python 1.py "a1bd@daeF"

import itertools
import sys

password = sys.argv[1]

def Size2(str_, size):
	tmp = []
	t = ""
	str_ = str_.lower()
	for s in str_:
		t += s
		if ord(s) in range(97,123):
			tmp.append(t)
			t = ""
	return tmp

def upper2(t, ChangeLen):
	tmp = []
	for i in itertools.combinations(range(len(t)),ChangeLen):
		s = t[:]
		for j in range(ChangeLen):
			s[i[j]] = s[i[j]].upper()
		tmp.append(s)
		s = ""
	return tmp

def all2(str_list):
	tmp = []
	for i in range(len(str_list) + 1):
		for j in upper2(t, i):
			tmp.append(j)
	return tmp

t = Size2(password,1)
str_list = all2(t)
for i in str_list:
	print ''.join(i)
