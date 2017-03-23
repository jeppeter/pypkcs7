#! /usr/bin/env python

import os
import sys

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

def _reload_pkcs7_debug_path(curpath):
	return _release_path_test(curpath,'__init_debug__.py')



topdir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..'))
_reload_pkcs7_path(topdir)

import extargsparse
import logging
import unittest
import re
import importlib
import tempfile
import subprocess
import platform
import random
import time
from pkcs7 import PKCS7Encoder
from pkcs7 import __version__ as pkcs7_version
from pkcs7 import __version_info__ as pkcs7_version_info
from disttools import release_file,release_get_catch


test_placer_holder=True

class debug_version_test(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    def test_A001(self):
    	verfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','VERSION')
    	vernum = '0.0.1'
    	with open(verfile,'r') as f:
    		for l in f:
    			l = l.rstrip('\r\n')
    			vernum = l
    	self.assertEqual(vernum , pkcs7_version)
    	sarr = re.split('\.',vernum)
    	self.assertEqual(len(sarr),3)
    	i = 0
    	while i < len(sarr):
    		sarr[i] = int(sarr[i])
    		self.assertEqual(pkcs7_version_info[i],sarr[i])
    		i += 1
    	return




def set_log_level(args):
    loglvl= logging.ERROR
    if args.verbose >= 3:
        loglvl = logging.DEBUG
    elif args.verbose >= 2:
        loglvl = logging.INFO
    elif args.verbose >= 1 :
        loglvl = logging.WARN
    # we delete old handlers ,and set new handler
    logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    return


def release_handler(args,parser):
	set_log_level(args)
	global topdir
	_reload_pkcs7_debug_path(os.path.join(topdir,'src','pkcs7'))
	mod = importlib.import_module('__init_debug__')
	includes = args.release_importnames
	logging.info('args %s includes %s'%(repr(args),includes))
	repls = dict()

	logging.info('includes %s repls %s'%(includes,repr(repls)))
	s = release_get_catch(mod,includes,[],repls)
	outs = slash_string(s)
	releaserepls = dict()
	releasekey = 'test_placer_holder'
	releasekey += '='
	releasekey += "True"
	releaserepls[releasekey] = outs
	logging.info('releaserepls %s'%(repr(releaserepls)))
	release_file(None,args.release_output,[],[],[],releaserepls)
	sys.exit(0)
	return

def test_handler(args,parser):
	set_log_level(args)
	testargs = []
	testargs.extend(args.subnargs)
	sys.argv[1:] = testargs
	unittest.main(verbosity=args.verbose,failfast=args.failfast)
	sys.exit(0)
	return

def slash_string(s):
	outs =''
	for c in s:
		if c == '\\':
			outs += '\\\\'
		else:
			outs += c
	return outs

def main():
	outputfile_orig = os.path.join(os.path.dirname(os.path.abspath(__file__)),'release.py')
	outputfile = slash_string(outputfile_orig)
	commandline_fmt = '''
		{
			"verbose|v" : "+",
			"failfast|f" : true,
			"release<release_handler>##release file##" : {
				"output|O" : "%s",
				"importnames|I" : ["debug_pkcs7_testcase","debug_pkcs7_rand_testcase"]
			},
			"test<test_handler>##test mode##" : {
				"$" : "*"
			}
		}
	'''
	commandline = commandline_fmt%(outputfile)
	options = extargsparse.ExtArgsOptions()
	parser = extargsparse.ExtArgsParse(options)
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line()
	return

if __name__ == '__main__':
	main()
