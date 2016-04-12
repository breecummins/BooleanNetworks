#!/bin/bash
# command line argument is directory with network files

for i in $( ls $1 ); do
	qsub python makedatabase $i