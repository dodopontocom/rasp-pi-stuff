#!/usr/bin/env python3

from hashlib import blake2b

message = "sometexthere".encode()
print("message: ", message)

print("BLAKE2B: ", blake2b(message).hexdigest())


