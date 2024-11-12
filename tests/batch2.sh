#!/bin/bash

echo "TOTAL NUMBER OF TESTS TO RUN: $#"
while [ $# -gt 0 ]; do
    nbjob run --tar zsc2_normal --qslot /SAS/ssmperf --class "CONTAINER&&SSMPERF&&CASCADELAKE&&48C&&768G" --log-file-dir /nfs/site/disks/simcloud_suihaich_001/nblogs --container-platform singularity --container-image oras://amr-registry.caas.intel.com/simics-containers-registry/sles12/interactive/sles12sp5interactive.sif:stable --work-dir $PWD --container-options "-B /nfs/site" --class-reservation 'disk=700' bash -c "perf stat -B -d -d -d record -o $1/perf.dump -- ./simics -batch-mode $1/test.simics; perf stat report -i $1/perf.dump | tee $1/perf.log"    
    shift
    if [ $# -gt 0 ]; then
        sleep 60
    fi
done



