#!/usr/bin/env python3

from hashlib import blake2b
from hmac import compare_digest

SECRET_KEY = "sometextheretogeneraterandomsecret".encode()
AUTH_SIZE = 32

def sign(cookie):
    h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
    h.update(cookie)
    return h.hexdigest().encode('utf-8')
    
def verify(cookie, sig):
        good_sig = sign(cookie)
        return compare_digest(good_sig, sig)
        
cookie = "user-alice".encode()
sig = sign("rodolfo".encode())
sig = sign(cookie)
print("{0},{1}".format(cookie, sig))
print("{0},{1}".format(cookie.decode('utf-8'), sig))
#user-alice,b'43b3c982cf697e0c5ab22172d1ca7421'
print(verify(cookie, sig))
print(verify(b'user-bob', sig))
print(verify(cookie, b'6a9e1f38f09cc8b5a6e8e589f3ad6c3ab2ae36aa1a7a9b8bc11dd7e57728fe8c'))



