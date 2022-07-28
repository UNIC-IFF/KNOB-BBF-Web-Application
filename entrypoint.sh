#!/bin/bash

echo "Running npm install..."
cd static && npm install

echo "Running npm install gulp-cli -g..."
cd static && npm install gulp-cli -g

echo "Running gulp..."
 gulp



echo "Running python /usr/src/app/app.py..."
cd ../ && python /usr/src/app/app.py
