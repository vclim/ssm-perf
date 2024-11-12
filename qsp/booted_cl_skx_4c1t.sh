#!/bin/bash

rm -rf booted_cl_skx_4c1t.ckpt
./simics targets/qsp-x86/qsp-clear-linux.simics num_cores=4 num_threads=1 cpu_comp_class="x86-skylake-server" -e 'bp.console_string.run-until object = board.serconsole.con string = "simics@cl-qsp ~ $"' -e 'write-configuration "booted_cl_skx_4c1t.ckpt" -independent-checkpoint' -batch-mode 
