#!/bin/bash

DATA=test_datasets
TESTCASE=("030102" "050110" "050201" "050202" "050210" "050305" "050311" "050312" "060106" "060108" "060201" "060207" "060211" "060302" "070205" "070308" "070403" "070409" "070605" "070608" "070610" "070611" "070702" "070704" "070708" "070710" "070902" "070911" "090105" "090206" "100205" "100211")

ZIP_030102=https://www.dropbox.com/s/ydtnhwvysg2fvvo/030102.zip?dl=0
ZIP_050110=https://www.dropbox.com/s/ld7zfoe9pr86qu2/050110.zip?dl=0
ZIP_050201=https://www.dropbox.com/s/9fb3hnd40rhz68d/050201.zip?dl=0
ZIP_050202=https://www.dropbox.com/s/k6lsp2rlmbedsyl/050202.zip?dl=0
ZIP_050210=https://www.dropbox.com/s/gk1b1bg4e931dsh/050210.zip?dl=0
ZIP_050305=https://www.dropbox.com/s/pcb1vwizq1uaxjz/050305.zip?dl=0
ZIP_050311=https://www.dropbox.com/s/utwec26vvjnmie5/050311.zip?dl=0
ZIP_050312=https://www.dropbox.com/s/si1c526uq7mg06j/050312.zip?dl=0
ZIP_060106=https://www.dropbox.com/s/0cw8zt71f8u4hy1/060106.zip?dl=0
ZIP_060108=https://www.dropbox.com/s/r84wv871l88zwj7/060108.zip?dl=0
ZIP_060201=https://www.dropbox.com/s/4cj57g1tm18mnr3/060201.zip?dl=0
ZIP_060207=https://www.dropbox.com/s/dxwt1ast6b3cetb/060207.zip?dl=0
ZIP_060211=https://www.dropbox.com/s/vwnucm61dlntp2b/060211.zip?dl=0
ZIP_060302=https://www.dropbox.com/s/nk32bsbfgycpp78/060302.zip?dl=0
ZIP_070205=https://www.dropbox.com/s/ificlxyaol943tv/070205.zip?dl=0
ZIP_070308=https://www.dropbox.com/s/x278nx4yxc01c9r/070308.zip?dl=0
ZIP_070403=https://www.dropbox.com/s/6ay4d8j56p3ugps/070403.zip?dl=0
ZIP_070409=https://www.dropbox.com/s/031mq094h37upot/070409.zip?dl=0
ZIP_070605=https://www.dropbox.com/s/wzhz2eubjcfnp8v/070605.zip?dl=0
ZIP_070608=https://www.dropbox.com/s/jte74l0eq1byazq/070608.zip?dl=0
ZIP_070610=https://www.dropbox.com/s/cva2x3tw9h3p7nh/070610.zip?dl=0
ZIP_070611=https://www.dropbox.com/s/b0vgj2yfgcfbgg1/070611.zip?dl=0
ZIP_070702=https://www.dropbox.com/s/7zof15nzxr1a7cq/070702.zip?dl=0
ZIP_070704=https://www.dropbox.com/s/nfahelwydczjfbe/070704.zip?dl=0
ZIP_070708=https://www.dropbox.com/s/2fctsxq21oidcd4/070708.zip?dl=0
ZIP_070710=https://www.dropbox.com/s/b6wixfagu0s1uq0/070710.zip?dl=0
ZIP_070902=https://www.dropbox.com/s/6va40eyyhog7l7t/070902.zip?dl=0
ZIP_070911=https://www.dropbox.com/s/7ymvccb7iurwvhf/070911.zip?dl=0
ZIP_090105=https://www.dropbox.com/s/maav9grhxukapkb/090105.zip?dl=0
ZIP_090206=https://www.dropbox.com/s/3bovmeiyka7yef5/090206.zip?dl=0
ZIP_100205=https://www.dropbox.com/s/lt1vd49tvqeom11/100205.zip?dl=0
ZIP_100211=https://www.dropbox.com/s/2fvabie5mtwsft1/100211.zip?dl=0

if [ $1 == "report" ]; then
	echo "report"  > "report.txt"
	for i in ${TESTCASE[@]}
	do
		str="cat experimental_results/${i}.txt  >> \"report.txt\""
		echo -ne "${i} "  >> "report.txt"
		eval $str
		echo ""  >> "report.txt"
	done
else
	for i in ${TESTCASE[@]}
	do
		if [ $1 -eq "${i}" ]; then
		   if [ ! -d "$DATA/${i}" ]; then
		   	   echo prepare ${i}
		   	   mkdir $DATA/${i}
		   	   if [ ! -f "${i}.zip" ]; then
				  mv $DATA/${1}.zip $DATA/${i}/
		   	   	  cd $DATA/${i}
		   	   	  unzip ${i}.zip
			   else
		   	   	  str="wget \$ZIP_${i} -O $DATA/${i}/${i}.zip"
		   	   	  echo $str
		   	   	  eval $str
		   	   	  cd $DATA/${i}
		   	   	  unzip ${i}.zip
			   fi			
		   fi
		fi
	done
fi
