#!/usr/bin/env python

import os
import sys

__version__ = "VERSIONNUMBER"
__version_info__ = "VERSIONINFO"


class PKCS7Encoder(object):
    '''
    RFC 2315: PKCS#7 page 21
    Some content-encryption algorithms assume the
    input length is a multiple of k octets, where k > 1, and
    let the application define a method for handling inputs
    whose lengths are not a multiple of k octets. For such
    algorithms, the method shall be to pad the input at the
    trailing end with k - (l mod k) octets all having value k -
    (l mod k), where l is the length of the input. In other
    words, the input is padded at the trailing end with one of
    the following strings:
             01 -- if l mod k = k-1
            02 02 -- if l mod k = k-2
                        .
                        .
                        .
          k k ... k k -- if l mod k = 0
    The padding can be removed unambiguously since all input is
    padded and no padding string is a suffix of another. This
    padding method is well-defined if and only if k < 256;
    methods for larger k are an open issue for further study.
    but we have the value
    '''
    def __init__(self, k=16):
        assert(k <= 256)
        assert(k > 1)
        self.__klen = k

    def __decode_inner(self,text):
        '''
        Remove the PKCS#7 padding from a text string
        '''
        nl = len(text)
        val = ord(text[-1])
        if nl > self.__klen:
            raise Exception('inner error len(%d) > %d'%(nl,self.__klen))

        # now check whether the code is the same
        delval = 0
        if val > 0 and val < self.__klen:
            delval = 1
            for i in range(val):
                curval = ord(text[nl-i-1])
                if curval != val:
                    delval=0
                    break
        if delval > 0:
            l = nl - val
        else:
            l = nl
        return text[:l]

    ## @param text The padded text for which the padding is to be removed.
    # @exception ValueError Raised when the input padding is missing or corrupt.
    def decode(self, text):
        dectext = ''
        if len(text) > self.__klen:
            i = 0
            while i < len(text):
                clen = len(text) - i
                if clen > self.__klen:
                    clen = self.__klen
                curtext = text[i:(i+clen)]
                dectext += self.__decode_inner(curtext)
                i += clen
        else:
            dectext = self.__decode_inner(text)
        return dectext

    def get_bytes(self,text):
        outbytes = []
        for c in text:
            outbytes.append(ord(c))
        return outbytes

    def get_text(self,inbytes):
        s = ''
        for i in inbytes:
            s += chr((i % 256))
        return s

    def __encode_inner(self,text):
        '''
        Pad an input string according to PKCS#7
        if the real text is bits same ,just expand the text
        '''
        totallen = len(text)
        passlen = 0
        enctext = ''
        #logging.info('all text (%s)'%(self.get_bytes(text)))
        while passlen < totallen:
            curlen = self.__klen
            if curlen > (totallen - passlen):
                curlen = (totallen - passlen)
            curtext = text[passlen:(passlen+curlen)]
            #logging.info('[%d] curtext (%s)'%(passlen,self.get_bytes(curtext)))
            val = ord(curtext[-1])
            addval = 0
            #logging.info('val %d curlen %d'%(val,curlen))
            if curlen == self.__klen and val > 0 and val < self.__klen:
                addval = 1
                for i in range(val):                    
                    curval = ord(curtext[curlen-i-1])
                    #logging.info('[%d]curval %d'%((-i),curval))
                    if curval != val:
                        addval = 0
                        break
            if addval != 0:
                passlen += (curlen - 1)
                enctext += curtext[:(curlen - 1)]
                enctext += chr(1)                
            else:
                if curlen < self.__klen:
                    enctext += curtext
                    for _ in range(self.__klen - curlen):
                        enctext += chr(self.__klen - curlen)
                else:
                    enctext += curtext
                passlen += curlen
            #logging.info('passlen %d'%(passlen))
        return enctext

    ## @param text The text to encode.
    def encode(self, text):
        return self.__encode_inner(text)


##importdebugstart
import unittest
import logging
import re
import random
import time

class debug_pkcs7_testcase(unittest.TestCase):
    def setUp(self):
        return
    def tearDown(self):
        return

    @classmethod
    def setUpClass(cls):
        return

    @classmethod
    def tearDownClass(cls):
        return

    def test_A001(self):
        inbytes=[0x89,0xc5,0xe8,0x32,0x74,0x6d,0x3e,0x41,0xe4,0x9c,0x4b,0x8a,0xcf,0xe6,0x4a,0x4d,0x10,0x80,0xef,0xd9,0x23,0xfe,0xdf,0x77,0x30,0xf9,0xc,0x7b,0xcc,0xad,0xc2,0x5b,0xce,0x17,0xfd,0x8,0x38,0x1d,0x5c,0xff,0x47,0x47,0x3f,0xc4,0xa1,0x36,0x57,0x2d,0x11,0x7c,0x73,0x2a,0x49,0x17,0xd5,0x93,0x9,0x74,0x95,0xac,0x6b,0xf5,0x97,0x69,0x21,0xd3,0xe9,0x80,0x5,0x9,0xb3,0x8f,0xee,0x1b,0x2a,0xec,0xac,0x91,0x69,0x1]
        k = 5
        pkcs7 = PKCS7Encoder(k)
        enctext = pkcs7.encode(pkcs7.get_text(inbytes))
        dectext = pkcs7.decode(enctext)
        outbytes = pkcs7.get_bytes(dectext)
        logging.info('input (%s) output (%s)'%(inbytes,outbytes))
        self.assertEqual(inbytes,outbytes)
        return

class debug_pkcs7_rand_testcase(unittest.TestCase):
    def setUp(self):
        return
    def tearDown(self):
        return

    @classmethod
    def setUpClass(cls):
        return

    @classmethod
    def tearDownClass(cls):
        return

    def __test_random(self,maxtimes):
        k = random.randint(2,255)
        pkcs7 = PKCS7Encoder(k)
        curmaxtimes = random.randint(1,maxtimes)
        for i in range(curmaxtimes):
            curlen = random.randint(1,maxtimes)
            curtext = ''
            for _ in range(curlen):
                curtext += chr(random.randint(0,255))
            enctext = pkcs7.encode(curtext)
            dectext = pkcs7.decode(enctext)
            logging.info('k(%d)[%d:%d]curtext (%s) enctext (%s) dectext(%s)'%(k,i,curmaxtimes,pkcs7.get_bytes(curtext),pkcs7.get_bytes(enctext),pkcs7.get_bytes(dectext)))
            self.assertEqual(dectext,curtext)
        return

    def test_A001(self):
        maxtimes = 100
        if 'RANDOM_PKCS7_NUM' in os.environ.keys():
            maxtimes = int(os.environ['RANDOM_PKCS7_NUM'])
        random.seed(time.time())
        for _ in range(maxtimes):
            self.__test_random(maxtimes)
        return


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))
import rtools

def debug_release():
    if '-v' in sys.argv[1:]:
        #sys.stderr.write('will make verbose\n')
        loglvl =  logging.DEBUG
        logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
    tofile= os.path.abspath(os.path.join(topdir,'pkcs7','__init__.py'))
    if len(sys.argv) > 2:
        for k in sys.argv[1:]:
            if not k.startswith('-'):
                tofile = k
                break
    versionfile = os.path.abspath(os.path.join(topdir,'VERSION'))
    if not os.path.exists(versionfile):
        raise Exception('can not find VERSION file')
    with open(versionfile,'r') as f:
        for l in f:
            l = l.rstrip('\r\n')
            vernum = l
            break
    sarr = re.split('\.',vernum)
    if len(sarr) != 3:
        raise Exception('version (%s) not format x.x.x'%(vernum))
    VERSIONNUMBER = vernum
    VERSIONINFO='( %s, %s, %s)'%(sarr[0],sarr[1],sarr[2])
    repls = dict()
    repls[r'VERSIONNUMBER'] = VERSIONNUMBER
    repls[r'"VERSIONINFO"'] = VERSIONINFO
    logging.info('repls %s tofile (%s)'%(repls.keys(),tofile))
    rtools.release_file('__main__',tofile,[r'^debug_*'],[[r'##importdebugstart.*',r'##importdebugend.*']],[],repls)
    return

def debug_main():
    if '--release' in sys.argv[1:]:
        debug_release()
        return
    if '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]:
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')

    if '--random' in sys.argv[1:]:
        i = 0
        for c in sys.argv[1:]:
            i += 1
            if c == '--random':
                break
        sys.argv[i] = 'debug_pkcs7_rand_testcase'
    unittest.main()
    return

if __name__ == '__main__':
    debug_main()
##importdebugend