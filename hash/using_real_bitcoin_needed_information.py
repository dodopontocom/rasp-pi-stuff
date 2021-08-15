#!/usr/bin/env python3

from hashlib import blake2b
from hmac import compare_digest
import json
import time
import subprocess

ur = str(subprocess.getoutput('cat /dev/urandom | tr -dc \'a-z0-9\' | fold -w 32 | head -n 1'))
S_KEY = ur + "_" + str(subprocess.getoutput('arch')) + "_" + str(subprocess.getoutput('lsb_release -cs'))
SECRET_KEY = S_KEY.encode('utf-8')
AUTH_SIZE = 32
difficulty = 4

f = open('sample.json',)
#f = open('another_block.json',)
data = json.load(f)

block_chain = []

def get_time():
    return time.time()

def isValidHashDifficulty(hash, difficulty):
    count = 0
    for i in hash:
        count += 1
        if(i != '0'):
            break
    return count > difficulty

def sign(block):
    nonce = 0
    block["nonce"] = nonce
    h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
    h.update(block)
    hash = h.hexdigest()
    while(not isValidHashDifficulty(hash, difficulty)):
        nonce = nonce + 1
        block["nonce"] = nonce
        h.update(block)
        hash = h.hexdigest()
    return hash

    
#def verify(cookie, sig):
#        good_sig = sign(cookie)
#        return compare_digest(good_sig, sig)
#        
#for c in data['transactions']:
#    cookie = json.dumps(c).encode('utf-8')
#    print(cookie)
#    sig_cookie = sign(cookie)
#    print(verify(cookie, sig_cookie))

def add_block(block):
    if (len(block_chain) == 0):
        #block["hash"] = sign(json.dumps(block).encode('utf-8'))
        block["hash"] = sign("{\'remetente\': \'John\', \'destinatario\': \'Peter\', \'mensagem\': \'300\'}".encode('utf-8'))
        block["confirmations"] = 1
        block["strippedsize"] = 2
        block["size"] = 2
        block["weight"] = 3
        block["height"] = 0
        block["version"] = 4
        block["versionHex"] = "0101"
        block["merkleroot"] = "6a"
        block["tx"] = "7b"

        block["time"] = get_time()
        block["mediantime"] = get_time()
        #block["nonce"] = 123456
        block["bits"] = "b"
        block["difficulty"] = 1
        block["chainwork"] = "9c"
        block["nTx"] = 1
        block["nextblockhash"] = "123"
        
    else:
        block["hash"] = sign(json.dumps(block).encode('utf-8'))
        last_block = block_chain[-1]
        block["previousblockhash"] = last_block["hash"]

        block["confirmations"] = 1
        block["strippedsize"] = 2
        block["size"] = 2
        block["weight"] = 3
        block["height"] = 0
        block["version"] = 4
        block["versionHex"] = "0101"
        block["merkleroot"] = "6a"
        block["tx"] = "7b"

        block["time"] = get_time()
        block["mediantime"] = get_time()
        #block["nonce"] = 123456
        block["bits"] = "b"
        block["difficulty"] = 1
        block["chainwork"] = "9c"
        block["nTx"] = 1
        block["nextblockhash"] = "123"        
        
    block_chain.append(block)

for t in data['transactions']:
    print("===")
    print(t)
    add_block(t)


print(block_chain)

#for v in block_chain:
#    cookie = json.dumps(v).encode('utf-8')
#    #print(cookie)
#    sig_cookie = sign(cookie)
#    print(verify(cookie, sig_cookie))
