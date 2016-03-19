#!/bin/python

def toDict( string1 ):
	l = string1.replace(", ", ",").split(",")
	d={};
	index=0
	for i in range(len(l)):
		d[ l[i] ] = index
		index+=1
	return d

f = open( "./tic-tac-toe.data", "r")
f1 = open( "./tic-tac-toe.mod.data", "w")

while True:
	l = f.readline()
	if len(l.strip()) == 0:
		break;
	l = l.replace('o,', '0,')
	l = l.replace('x,', '1,')
	l = l.replace('b,', '2,')
	f1.write(l);

f.close();
f1.close();
