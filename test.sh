#!/bin/sh

str="docker run --name=NIA-SSP --runtime=nvidia --rm -v $PWD/test_datasets:/ssp/data -v $PWD/experimental_results:/ssp/experimental_results nia-ssp:0.9 python valid.py --datacfg data/$1/$1.data --modelcfg data/$1/models/yolo-pose.cfg --weightfile data/$1/models/model.weights"
echo $str
eval $str
