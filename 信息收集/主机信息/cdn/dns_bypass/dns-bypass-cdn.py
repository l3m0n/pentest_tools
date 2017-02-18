#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#__author__ == Tr3jer_CongRong

import re
import sys
import time
import threading
import dns.resolver

class Bypass_CDN:

    def __init__(self,domain,dns_dict):
        self.domain = domain
        self.myResolver = dns.resolver.Resolver()
        self.dns_list = set([d.strip() for d in open(dns_dict)])
        self.good_dns_list,self.result_ip = set(),set()

    def test_dns_server(self,server):
        self.myResolver.lifetime = self.myResolver.timeout = 2.0
        try:
            self.myResolver.nameservers = [server]
            sys.stdout.write('[+] Check Dns Server %s \r' % server)
            sys.stdout.flush()
            answer = self.myResolver.query('google-public-dns-a.google.com')
            if answer[0].address == '8.8.8.8':
                self.good_dns_list.add(server)
        except:
            pass

    def load_dns_server(self):
        print '[+] Load Dns Servers ...'
        threads = []
        for i in self.dns_list:
            threads.append(threading.Thread(target=self.test_dns_server,args=(i,)))
        for t in threads:
            t.start()
            while True:
                if len(threading.enumerate()) < len(self.dns_list) / 2:
                    break
                else:
                    time.sleep(1)
        print '\n[+] Release The Thread ...'
        for j in threads: j.join()
        print '[+] %d Dns Servers Available' % len(self.good_dns_list)

    def ip(self,dns_server):
        self.myResolver.nameservers = [dns_server]
        try:
            result = self.myResolver.query(self.domain)
            for i in result:
                self.result_ip.add(str(i.address))
        except:
            pass

    def run(self):
        self.load_dns_server()
        print '[+] Dns Servers Test Target Cdn ...'
        threads = []
        for i in self.good_dns_list:
            threads.append(threading.Thread(target=self.ip,args=(i,)))
        for t in threads:
            t.start()
            while True:
                if len(threading.enumerate()) < len(self.good_dns_list) / 2:
                    break
                else:
                    time.sleep(1)
        for j in threads: j.join()
        for i in self.result_ip: print i

if __name__ == '__main__':
    dns_dict = 'foreign_dns_servers.txt'
    bypass = Bypass_CDN(sys.argv[1],dns_dict)
    bypass.run()