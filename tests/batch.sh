#!/bin/bash

./batch1.sh `ls $1/*/ -d`
./batch2.sh `ls $1/.*_*/ -d`


