#coding: utf-8

import time,re
import requests
import base64 
from conf import web_port,callback_mail
from mail import send_mail 
init_data = ''
padding = '~~~~~~~'
#配置项

#设置每个几秒请求一次,默认20秒
sleep_time = 20

#设置你需要读取数据的地址，可以使用在线记事本、博客、论坛等功能,此处使用了xnote
server = 'http://www.xnote.cn/note/53094884/'
headers = {'cookie':'yourcookie'}

def sower(data):
	url = 'http://127.0.0.1:%s/compare'%(web_port)
	try:
		response = requests.post(url,data=data,timeout=2,verify=False)
		print response.content
	except Exception, e:
		send_mail(callback_mail,'post to 127.0.0.1 failed',str(e))
def get_data(url,headers):
	global init_data
	try:
		response = requests.get(url,headers=headers,timeout=5,verify=False)
		new_data = base64.b64decode(re.findall(r'%s(.*?)%s'%(padding,padding),response.content)[0])
		if new_data and new_data != init_data:
			print new_data
			init_data = new_data
			sower(new_data)
	except Exception,e:
		send_mail(callback_mail,'get data failed',str(e))

if __name__ == '__main__':
	while True:
		get_data(server,headers)
		time.sleep(sleep_time)