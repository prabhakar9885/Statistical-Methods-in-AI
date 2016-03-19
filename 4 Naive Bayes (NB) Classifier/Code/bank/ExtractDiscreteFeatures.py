#!/bin/python

import sys

fileName = sys.argv[1]

f = open(fileName, "r")
mod = open(fileName+"-mod", "w+")
l = f.readline()

c=0
while True:
	c+=1;
	l = f.readline()
	if len(l) == 0:
		break
	l = l.split(";")
	words=[]
	
	for i in l:
		if i.replace('-','').isdigit() == False:
			words.append(i)

	mod.write( ','.join(words) )

mod.close()