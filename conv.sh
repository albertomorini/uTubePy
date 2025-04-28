#!/bin/bash

source ~/.bashrc
shopt -s expand_aliases

for i in ./output/*;
do
 	echo "$i";
	convertToM4A "$i"

done
