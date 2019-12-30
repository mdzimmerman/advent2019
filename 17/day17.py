#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 17:20:41 2019

@author: mzimmerman
"""

import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode
#from point import Point

class Grid:
    def __init__(self, data):
        self.data = data
        
    @classmethod
    def from_intcode(self, intcode):
        pass
    
    @classmethod
    def from_file(self, filename):
        pass


if __name__ == '__main__':
    pass