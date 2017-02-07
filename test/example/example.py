#! /usr/bin/env python

import sys
import os

def _release_path_test(curpath,*paths):
    testfile = os.path.join(curpath,*paths)
    if os.path.exists(testfile):
        if curpath != sys.path[0]:
            if curpath in sys.path:
                sys.path.remove(curpath)
            oldpath=sys.path
            sys.path = [curpath]
            sys.path.extend(oldpath)
    return

def _reload_pkcs7_path(curpath):
	return _release_path_test(curpath,'pkcs7','__init__.py')

topdir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..'))
_reload_pkcs7_path(topdir)

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