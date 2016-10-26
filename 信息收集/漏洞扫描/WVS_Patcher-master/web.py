# encoding:utf-8

import os, subprocess
from multiprocessing import Process, Queue
from bottle import route, run, template, request

from conf import web_port, queue_num, callback_mail, wvs_save_dir
queue_waiting = Queue()
queue_scaning = Queue(queue_num)


@route('/compare', method='POST')
def compare_scaner():    
    urls = request.POST.url.split('\n')

    for url in urls:
        url = url.strip()
        if url:
            queue_waiting.put(url)

    return {
        "msg": 'Adding %d tasks' % len(urls),
        "callback_mail": callback_mail
    }


@route('/index', method='GET')
def index():
    return template('index.html', scaning_count=queue_scaning.qsize(), waiting_count=queue_waiting.qsize())


@route('/expire', method='GET')    
def expire():
    queue_scaning.get()

    return 'expire success!'


def queue_get(queue_waiting, queue_scaning):
    while True:
        url = queue_waiting.get()

        queue_scaning.put(1)
        print "Scaning: %s" % url
        subprocess.Popen("python wvs.py -u \"%s\"" % url, shell=True)

        
if __name__ == '__main__':
    if not os.path.exists(wvs_save_dir):
        os.mkdir(wvs_save_dir)

    Process(target=queue_get, args=(queue_waiting, queue_scaning)).start()
    run(host='0.0.0.0', port=web_port)