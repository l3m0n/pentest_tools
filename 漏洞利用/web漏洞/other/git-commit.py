#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import requests
import os
import zlib
import re
import Queue
import binascii

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MB526 "
        "Build/4.5.1-134_DFP-1321) AppleWebKit/533.1 (KHTML, like Gecko)"
        " Version/4.0 Mobile MQQBrowser/4.0 Safari/533.1"
}
target = sys.argv[1]
output_folder = "./xdsec_cms/"

class GitDdatabase(object):
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def read_to_next_char(self, char=" "):
        pos = self.data.index(char, self.pos)
        ret = self.read_exact(pos)
        self.pos += 1
        return ret

    def read_exact(self, size):
        ret = self.data[self.pos:size]
        self.pos = size
        return ret

    def read_blob(self):
        return re.sub('^blob \d+?\00', '', self.data)

    def read_tree(self):
        mode = self.read_to_next_char(" ")
        filename = self.read_to_next_char("\x00")
        sha1 = self.read_exact(self.pos + 20)
        return mode, filename, sha1

    def get_db_type(self):
        file_sort = self.read_to_next_char(" ")
        file_size = self.read_to_next_char("\x00")
        file_size = int(file_size)
        return file_sort, file_size

def request_object(id):
    global target
    folder = 'objects/%s/' % id[:2]
    response = requests.get(target + folder + id[2:])
    if response.status_code == 200:
        return zlib.decompress(response.content)
    else:
        return False

if __name__ == "__main__":
    response = requests.get(target + "refs/tags/1.0", headers=headers)
    if response.status_code == 404:
        print("No this tag")
        sys.exit(0)
    data = response.content
    commit_id = data.strip()

    next_id = commit_id
    data = request_object(next_id)
    if not data:
        print("No this commit id")
        sys.exit(0)

    rex = re.search(ur"commit .*?([a-f0-9]{40})", data)
    next_id = rex.group(1)
    data = request_object(next_id)
    if not data:
        print("No this commit id")
        sys.exit(0)

    tasks = Queue.Queue()
    gd = GitDdatabase(data)
    file_sort, file_size = gd.get_db_type()
    while 1:
        try:
            (mode, filename, sha1) = gd.read_tree()
            basedir = "./"
            tasks.put((mode, filename, sha1, basedir))
        except ValueError as e:
            break

    while 1:
        if tasks.empty():
            break
        (mode, filename, sha1, basedir) = tasks.get()
        sha1 = binascii.b2a_hex(sha1)
        data = request_object(sha1)
        if not data:
            continue

        gd = GitDdatabase(data)
        file_sort, file_size = gd.get_db_type()
        if file_sort == "tree":
            basedir = os.path.join(basedir, filename)
            while 1:
                try:
                    (mode, filename, sha1) = gd.read_tree()
                    tasks.put((mode, filename, sha1, basedir))
                except ValueError as e:
                    break
        elif file_sort == "blob":
            data = gd.read_blob()
            folder = os.path.join(output_folder, basedir)
            if not os.path.exists(folder):
                os.makedirs(folder)
            filename = os.path.join(folder, filename)
            with open(filename, "wb") as f:
                f.write(data)
            print("[+] Write {filename} success".format(filename=filename))
