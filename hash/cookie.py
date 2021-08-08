#!/usr/bin/env python3

from hashlib import blake2b
from hmac import compare_digest
import json
import time

SECRET_KEY = "sometextheretogeneraterandomsecret".encode()
AUTH_SIZE = 32

chain = [
            {
                "remetente": "John",
                "destinatario": "Peter",
                "mensagem": "300"
            },
            {
                "remetente": "Henry",
                "destinatario": "Paul",
                "mensagem": "120"
            }

        ]
block_chain = []
def get_time():
    return time.time()

def sign(cookie):
    h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
    h.update(cookie)
    return h.hexdigest()
    
def verify(cookie, sig):
        good_sig = sign(cookie)
        return compare_digest(good_sig, sig)
        
for c in chain:

    cookie = json.dumps(c).encode()
    sig_cookie = sign(cookie)
    #print(verify(cookie, sig_cookie))

def add_block(block):
    if (len(block_chain) == 0):
        block["timestamp"] = get_time()
        block["hash"] = sign(json.dumps(block).encode())
    else:
        block["timestamp"] = get_time()
        last_block = block_chain[-1]
        block["last_hash"] = last_block["hash"]
        block["hash"] = sign(json.dumps(block).encode())
    block_chain.append(block)

for t in chain:
    add_block(t)

print(block_chain)

for v in block_chain:
    cookie = json.dumps(v).encode()
    sig_cookie = sign(cookie)
    print(verify(cookie, sig_cookie))
