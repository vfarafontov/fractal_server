#!/bin/bash

DEFAULT_PORT="8888"
PORT=$1

./kill

if [ $PORT ]
	then
		SELECTED_PORT=$1
	else
		SELECTED_PORT=$DEFAULT_PORT
fi

echo "INFO - Starting fractal server on" $SELECTED_PORT
python bin/image_serve.py $SELECTED_PORT &
echo "OK - Done"
