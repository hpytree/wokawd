#!/usr/bin/bash
[ -d build ] || mkdir build
cp -ri src/* build
rm build/wormv.cpp build/wormv.py
g++ -o build/wormv src/wormv.cpp -pthread
chmod 777 -R build/
