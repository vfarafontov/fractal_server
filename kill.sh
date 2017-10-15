#!/bin/bash

echo "INFO - Killing snakes"
ps aux | grep python | grep -v "grep python bin" | awk '{print $2}' | xargs kill -9
echo "OK - Done"
