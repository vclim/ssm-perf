#!/bin/bash

## this script automates the steps from https://nova.intel.com/documentation/guided_examples/lua-sde/

mkdir .taf -p
cp config_sde_example.yaml .taf/config.yaml
sed -i "s/PWD/$current_dir/g" .taf/config.yaml

./taf validate workload workload_sde_example.yaml
./taf validate config .taf/config.yaml

# check tools
./taf info --tools --config .taf/config.yaml

# recording - executes the workload and captures a pinball of the Region of Interest (ROI), which in our case, is the entire run.
rm -rf efforts/sde_example
./taf start --name sde_example --workload workload_sde_example.yaml --config .taf/config.yaml --stop recording --siliconless

# report
./taf report -o report --name sde_example

# recording profile - During the recording_profile step, the ROI is divided into equal-sized slices, and a profile is generated for each one
./taf resume --workdir . --config .taf/config.yaml --name sde_example --stop recording_profile

# Choosing Representative Traces - In the trcset_select step, we’ll cluster the slices from the previous step and choose a representative slice for each cluster. These representatives will form our selected traces.
./taf resume --workdir . --config .taf/config.yaml --name sde_example --stop trcset_select

# Collecting Traces
./taf resume --workdir . --config .taf/config.yaml --name sde_example --stop trcset

# Ensuring Trace Validity (A trace is deemed functionally valid if it successfully simulates in zsim and its final instruction pointer (IP) matches the IP reported by SDE)
./taf resume --workdir . --config .taf/config.yaml --name sde_example --stop trcset_check

# simulate the traces (coho)
./taf resume --workdir . --config .taf/config.yaml --name sde_example --stop trcset_profile


./taf show --history --name sde_example
