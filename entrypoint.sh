#!/bin/bash

echo "Running npm install..."
npm install

echo "Running npm install gulp-cli -g..."
npm install gulp-cli -g

echo "Running gulp..."
gulp


echo "Running python /usr/src/app/app.py..."
python /usr/src/app/app.py
