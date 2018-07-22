##!/usr/bin/env python

from scale.scale import Scale
from labelwriter.labelwriter import Labelwriter

def main():
    print("running processhall application")
    myscale = Scale('192.168.1.4','4001')

if __name__ == '__main__':
    main()