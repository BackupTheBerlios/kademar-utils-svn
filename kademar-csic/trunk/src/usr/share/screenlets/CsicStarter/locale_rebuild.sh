#/bin/bash

# Create files using xgettext

MSGFMT=msgfmt
DIR=$(dirname "$0")/locale

for i in $(find "$DIR" -name *.po); do
	echo "Building $i..."
	$MSGFMT "$i" -o "$(echo "$i" | sed s/.po/.mo/)"
done