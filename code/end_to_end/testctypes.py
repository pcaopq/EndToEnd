#!/usr/bin/env python

import ctypes

def main():
    # my_test_lib = ctypes.cdll.LoadLibrary('/home/usrname/test.so')
    my_test_lib = ctypes.cdll.LoadLibrary('test.so')
    for i in range(10):
        # Note, this uses the Python 2 print 
        print "Random = %d" % my_test_lib.get_random(1, 10)

if __name__ == '__main__':
    main()
