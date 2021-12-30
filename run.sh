#!/bin/sh

# 1) build
./build.sh

# 2) prepare all
./prepare.sh 070308
./prepare.sh 070610
./prepare.sh 050311

# 3) test all
./test.sh 070308
./test.sh 070610
./test.sh 050311
