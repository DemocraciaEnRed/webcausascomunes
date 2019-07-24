#!/bin/bash
FILES="$@"
for i in $FILES
do
	echo "Prcoessing image $i ..."
	extension="${i##*.}"
	filename="${i%.*}"
	/usr/bin/convert -thumbnail 920 $i carousel/car-$filename.png
done
