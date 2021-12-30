#!/bin/sh

# 1) build
./build.sh

# 2) prepare all
./prepare.sh 030102
./prepare.sh 050110
./prepare.sh 050201
./prepare.sh 050202
./prepare.sh 050210
./prepare.sh 050305
./prepare.sh 050311
./prepare.sh 050312
./prepare.sh 060106
./prepare.sh 060108
./prepare.sh 060201
./prepare.sh 060207
./prepare.sh 060211
./prepare.sh 070205
./prepare.sh 070308
./prepare.sh 070403
./prepare.sh 070409
./prepare.sh 070605
./prepare.sh 070608
./prepare.sh 070610
./prepare.sh 070611
./prepare.sh 070702
./prepare.sh 070704
./prepare.sh 070708
./prepare.sh 070710
./prepare.sh 070902
./prepare.sh 070911
./prepare.sh 090105
./prepare.sh 090206
./prepare.sh 100205
./prepare.sh 100211

# 3) test all
./test.sh 030102
./test.sh 050110
./test.sh 050201
./test.sh 050202
./test.sh 050210
./test.sh 050305
./test.sh 050311
./test.sh 050312
./test.sh 060106
./test.sh 060108
./test.sh 060201
./test.sh 060207
./test.sh 060211
./test.sh 070205
./test.sh 070308
./test.sh 070403
./test.sh 070409
./test.sh 070605
./test.sh 070608
./test.sh 070610
./test.sh 070611
./test.sh 070702
./test.sh 070704
./test.sh 070708
./test.sh 070710
./test.sh 070902
./test.sh 070911
./test.sh 090105
./test.sh 090206
./test.sh 100205
./test.sh 100211
