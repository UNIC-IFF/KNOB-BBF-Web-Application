#!/bin/bash

echo "Running npm install..."
cd static && npm install

echo "Running npm install gulp-cli -g..."
cd static && npm install gulp-cli -g

echo "Running gulp..."
cd static && gulp


echo "Running python /usr/src/app/app.py..."
python /usr/src/app/app.py
