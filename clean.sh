#! /bin/bash

_script_file=`python -c "import sys;import os;print('%s'%(os.path.abspath(sys.argv[1])));" "$0"`
script_dir=`dirname $_script_file`

rm -rf $script_dir/dist
rm -rf $script_dir/pkcs7

rm -f $script_dir/test/release/release.py.touched

rm -f $script_dir/src/pkcs7/__init_debug__.pyc
rm -f $script_dir/test/release/release.py
rm -f $script_dir/rtools.pyc

rm -rf $script_dir/__pycache__/
rm -rf $script_dir/src/pkcs7/__pycache__/
rm -rf $script_dir/pkcs7.egg-info/

rm -f $script_dir/setup.py

