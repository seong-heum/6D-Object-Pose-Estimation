#!/bin/sh

#str="docker run --name=NIA-SSP --runtime=nvidia --rm -v $PWD/test_datasets/data:/ssp/data -v $PWD/test_datasets/cfg:/ssp/cfg nia-ssp:0.5 python valid.py --datacfg data/$1/070308.data --modelcfg cfg/yolo-pose.cfg --weightfile data/$1/models/model.weights"
str="docker run --name=NIA-SSP --runtime=nvidia --rm -v $PWD/test_datasets/data:/ssp/data -v $PWD/test_datasets/cfg:/ssp/cfg ssuvip/nia-ssp:latest python valid.py --datacfg data/$1/070308.data --modelcfg cfg/yolo-pose.cfg --weightfile data/$1/models/model.weights"
echo $str
eval $str
