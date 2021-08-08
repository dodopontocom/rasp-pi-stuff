#!/usr/bin/env python3

from hashlib import blake2b
from hmac import compare_digest
import json
import time
import subprocess

S_KEY = str(subprocess.getoutput('arch')) + "_" + str(subprocess.getoutput('lsb_release -cs'))
SECRET_KEY = S_KEY.encode('utf-8')
AUTH_SIZE = 32

#chain = [
#            {
#                "remetente": "John",
#                "destinatario": "Peter",
#                "mensagem": "300"
#            },
#            {
#                "remetente": "Henry",
#                "destinatario": "Paul",
#                "mensagem": "120"
#            }
#
#        ]
f = open('sample.json',)
data = json.load(f)

block_chain = []

def get_time():
    return time.time()

def sign(cookie):
    h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
    h.update(cookie)
    return_cookie = h.hexdigest()
    return return_cookie
    
def verify(cookie, sig):
        good_sig = sign(cookie)
        return compare_digest(good_sig, sig)
        
for c in data['chain']:
    cookie = json.dumps(c).encode('utf-8')
    print(cookie)
    sig_cookie = sign(cookie)
    print(verify(cookie, sig_cookie))

def add_block(block):
    if (len(block_chain) == 0):
        block["timestamp"] = get_time()
        block["hash"] = sign(json.dumps(block).encode('utf-8'))
    else:
        block["timestamp"] = get_time()
        last_block = block_chain[-1]
        block["last_hash"] = last_block["hash"]
        block["hash"] = sign(json.dumps(block).encode('utf-8'))
    block_chain.append(block)

for t in data['chain']:
    add_block(t)

print(block_chain)

for v in block_chain:
    cookie = json.dumps(v).encode('utf-8')
    sig_cookie = sign(cookie)
    print(verify(cookie, sig_cookie))
