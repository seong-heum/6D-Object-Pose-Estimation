#!/bin/sh

DATA=test_datasets
OBJ_070308=$DATA/070308
OBJ_070610=$DATA/070610
OBJ_050311=$DATA/050311

if [ ! -d "$DATA" ]; then
	mkdir $DATA
fi


if [ $1 -eq "070308" ]; then
   if [ ! -d "$OBJ_070308" ]; then
   	   echo Preparing 070308
   	   mkdir $OBJ_070308
   	   str="wget https://www.dropbox.com/s/x278nx4yxc01c9r/070308.zip?dl=0 -O $OBJ_070308/070308.zip"
   	   echo $str
   	   eval $str
   	   cd $OBJ_070308
   	   unzip 070308.zip
   fi
fi


if [ $1 -eq "070610" ]; then
   if [ ! -d "$OBJ_070610" ]; then
   	   echo Preparing 070610
   	   mkdir $OBJ_070610
   	   str="wget https://www.dropbox.com/s/cva2x3tw9h3p7nh/070610.zip?dl=0 -O $OBJ_070610/070610.zip"
   	   echo $str
   	   eval $str
   	   cd $OBJ_070610
   	   unzip 070610.zip
   fi
fi


if [ $1 -eq "050311" ]; then
   if [ ! -d "$OBJ_050311" ]; then
   	   echo Preparing 050311
   	   mkdir $OBJ_050311
   	   str="wget https://www.dropbox.com/s/utwec26vvjnmie5/050311.zip?dl=0 -O $OBJ_050311/050311.zip"
   	   echo $str
   	   eval $str
   	   cd $OBJ_050311
   	   unzip 050311.zip
   fi
fi
