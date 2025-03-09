
source ~/Documents/shell/shellConfig;

for i in ./output/*;
do
 	echo "$i";
	convertToM4A "$i"

done
