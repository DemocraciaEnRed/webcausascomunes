#!/bin/bash
FILES="$@"
for i in $FILES
do
	echo "Prcoessing image $i ..."
	/usr/bin/convert -thumbnail 332 $i thumbs/thumb-$i
done
