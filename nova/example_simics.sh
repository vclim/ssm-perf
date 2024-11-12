#!/bin/bash

## this script automates the steps from https://nova.intel.com/documentation/guided_examples/openssl_speed_simics_multicore/

#echo ../../2096/6.0.87 > .package-list
#echo ../../4094/6.0.16 >> .package-list
#echo ../../8112/6.0.29 >> .package-list
#echo ../../1033/6.0.6  >> .package-list
#echo ../../1030/6.0.18 >> .package-list
#/nfs/site/disks/central_release_tree/sles11/simics/packages/1000/6.0.209/bin/project-setup --ignore-existing-files
#./simics targets/qsp-x86/qsp-clear-linux.simics num_cores=2 num_threads=2 cpu_comp_class="x86-alderlake" -e 'bp.console_string.run-until object = board.serconsole.con string = "simics@cl-qsp ~ $"' -e 'write-configuration "booted.ckpt" -independent-checkpoint' -batch-mode -no-win

cp ../qsp/.package-list .
/nfs/site/disks/central_release_tree/sles11/simics/packages/1000/6.0.209/bin/project-setup --ignore-existing-files
../qsp/booted_cl_skx_4c1t.sh

# fix taf config file
current_dir=$(echo "$PWD" | sed 's/[\/&]/\\&/g')
mkdir .taf -p
cp config_simics_example.yaml .taf/config.yaml
sed -i "s/PWD/$current_dir/g" .taf/config.yaml 
sed -i "s/PWD/$current_dir/g" workload_simics_example.yaml

# validate
./taf validate  config .taf/config.yaml
./taf validate workload_definition workload_simics_example.yaml

# run
rm -rf efforts/simics_example
./taf start --name simics_example --flow SIMICS_MULTICORE --workload workload_simics_example.yaml

# post
./taf report -o report --name simics_example
./taf bundle checkpoints -o bundle --name simics_example

./taf show --history --name simics_example
