#! /usr/bin/env python
#coding=utf-8

class Dump:
    def __init__(self,param='w'):
        self.output=open('dump.txt',param)
        
    def writeline(self,line):
        self.output.write('%s\n' %line)