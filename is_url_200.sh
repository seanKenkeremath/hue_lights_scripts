#!/bin/bash

URL=$1
CONTROL_OUTPUT=$(curl -sI http://www.google.com | grep "HTTP/1.1")
OUTPUT=$(curl -sI $URL | grep "HTTP/1.1")
if [ "$OUTPUT" == *200* ]
	then
	echo "1"
else
	echo "0"
fi