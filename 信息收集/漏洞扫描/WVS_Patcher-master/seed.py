#coding: utf-8
import sys,os
import base64
from urllib import quote
padding = '~~~~~~~'
output = './output.txt'


def usage():
	print 'usage:'
	print 'seed.py --url www.baidu.com'
	print 'seed.py --file any_file.txt'
	sys.exit()


if __name__ == '__main__':
	if len(sys.argv) != 3:
		usage()
	if sys.argv[1] == '--url':
		url = 'url=%s'%(sys.argv[2])
		print padding+base64.b64encode(url)+padding
	elif sys.argv[1] == '--file':
		f = open(sys.argv[2],'r')
		content = f.read().strip()
		f.close()
		url = 'url=%s'%(quote(content))
		f = open(output,'w')
		f.write(padding+base64.b64encode(url)+padding)
		f.close()
		print 'saved to %s'%(output)
	else:
		usage()
