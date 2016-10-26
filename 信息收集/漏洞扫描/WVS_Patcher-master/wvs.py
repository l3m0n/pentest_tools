# encoding: utf-8
import sys, getopt, random, requests, subprocess
from xml.dom import minidom

from mail import send_mail
from conf import callback_mail, expire_url
from conf import wvs_location, wvs_save_dir, wvs_scan_sentence
from conf import filter


class wvs_scan():
    target = ''
    task_id = 0
    save_dir = ''
    scan_sentence = ''
    result = ''

    def __init__(self, target):
        self.target = target
        self.task_id = random.randint(10000, 100000)
        self.save_dir = wvs_save_dir + (str(self.task_id)) + '/'
        self.scan_sentence = wvs_scan_sentence % (target, self.save_dir)

    def do_scan(self):
        res = subprocess.Popen(wvs_location + 'wvs_console.exe ' + self.scan_sentence, shell=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        (output, error) = res.communicate()     # 阻塞，等待扫描结束
        requests.get(expire_url)                # 释放扫描队列

        if error:
            sys.exit(error)

        self.result = {"target": self.target, "scan_result": {}}
        self.result['scan_result'] = self.parse_xml(self.save_dir + 'export.xml')


    def parse_xml(self, file_name):
        bug_list = {}

        try:
            root = minidom.parse(file_name).documentElement
            ReportItem_list = root.getElementsByTagName('ReportItem')
            bug_list['time'] = root.getElementsByTagName('ScanTime')[0].firstChild.data.encode('utf-8')
            bug_list['bug'] = []

            if ReportItem_list:
                for node in ReportItem_list:
                    color = node.getAttribute("color")
                    name = node.getElementsByTagName("Name")[0].firstChild.data.encode('utf-8')
                    if color in filter['color_white_list'] and name not in filter['bug_black_list']:
                        temp = {}
                        temp['name'] = name
                        temp['color'] = color.encode('utf-8')
                        temp['details'] = node.getElementsByTagName("Details")[0].firstChild.data.encode('utf-8')
                        temp['affect'] = node.getElementsByTagName("Affects")[0].firstChild.data.encode('utf-8')

                        bug_list['bug'].append(temp)

        except Exception, e:
            sys.exit("Error in parse_xml: %s" % e)

        return bug_list

    def do_callback(self):
        result = self.result

        if callback_mail:
            cont = ('对 %s 的WVS扫描结果（扫描时间 %s）如下：<br/><br/><table border=1 cellpadding=0 cellspacing=0>'
                    '<tr><td>漏洞名称</td><td>等级</td><td>细节</td><td>URL</td></tr>') \
                   % (result['target'], result['scan_result']['time'])

            for bug in result['scan_result']['bug']:
                cont += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % \
                        (bug["name"], bug["color"], bug["details"], bug["affect"])

            cont += '</table>'

            send_mail(callback_mail, '[WVS_Result] %s' % self.target, cont)


    def run(self):
        self.do_scan()
        self.do_callback()


if __name__ == '__main__':
    url = ''
    opts, args = getopt.getopt(sys.argv[1:], "u:")

    for op, value in opts:
        if op == "-u":
            url = value

    wvs_scan(url).run()
