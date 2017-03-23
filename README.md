# pkcs7
> python package pkcs7 conform for the [RFC5652](https://tools.ietf.org/html/rfc5652#section-6.3)

### Release History
* Mar 23th 2017 Release 0.1.2 to fixup the bug not according to pkcs7 protocol
* Feb 8th 2017 Release 0.1.0 to release first version of pkcs7

### install
* in linux or unix-like system
```shell
sudo pip install pkcs7
```

* in windows
```shell
pip install pkcs7
```

### example
* file example.py
```python
#! /usr/bin/env python

import sys
from pkcs7 import PKCS7Encoder

def pkcs7_encode(text,k=16):
    pkcs7 = PKCS7Encoder(k)
    return pkcs7.encode(text)

def pkcs7_decode(text,k=16):
    pkcs7 = PKCS7Encoder(k)
    return pkcs7.decode(text)

def main():
    for c in sys.argv[1:]:
        enc = pkcs7_encode(c)
        dec = pkcs7_decode(enc)
        print('[%s] enc => [%s] dec => [%s]'%(repr(c),repr(enc),repr(dec)))
    return

if __name__ == '__main__':
    main()
```

* command
```shell
python example.py  examplecc6342223345533222
```

* output
```text
['examplecc6342223345533222'] enc => ['examplecc6342223345533222\x07\x07\x07\x07\x07\x07\x07'] dec => ['examplecc6342223345533222']
```