#!/bin/bash

shopt -s expand_aliases
source ~/.bashrc

for i in ./output/*;
do
 	echo "$i";
	convertToM4A "$i"

done
