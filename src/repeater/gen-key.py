#!/usr/bin/python3

import hashlib
import sys

passw = sys.argv[1]

encoded = passw.encode()
result = hashlib.sha256(encoded)
print(result.hexdigest())