# For ESXi we need to reuse the autogen test, because it requires invoking the esxi_debug_enable() function after bios boots

from simmod.pylib import create
from simmod.srv_tests import env
import cli

simenv.log_dir = env.get_script_dir()
simenv.target = "oakstream/1_socket_ucc-generic" # aunit-bmc-cbbpunit-ese-imhpunit-oobmsm-pfrprot-s3m"
simenv.esxi_ver = "8.0.2"

platf_params = {
    'init_testers': True,
    'log_dir': simenv.log_dir,
    'os_type': 'esxi800',
    'ifwi_product_type': 'consumer',
    'os_product_type': 'consumer',
    'ifwi_build_type': ['release'],
    'test_desc': 'Boot to ESXI 8.0.1 (debug image).',
    'os_build_type': 'debug',
    'os_version': 'U2-EA2-11372496',
    'networking:create_network': True,
    'networking:i82599_present': True,
    'ESXI_VERSION_STR': '8.0.2',
    'perf_profile': 'default,direct_rdtsc',
#    'n_cores': 8, # to match the setting in https://hsdes.intel.com/appstore/article/#/15015544919
#    'disk_image': "/nfs/site/disks/ssg_stc_simics_workloads/artifactory/simics-repos/ts/images/dmr/esxi/ESXi_DMR_with_Magic_Ins_11.craff" #"/nfs/site/disks/simcloud_ashanx_002/narrow_down/UDISK/ESXi_DMR_with_Magic_Ins_11.craff",
#    'knobs:bios_knobs': 'disable_c6',
#    'knobs:bios_knobs_string': 'AcpiC2Enumeration=0,AcpiC3Enumeration=0',
#    'enabled_acp_mask': '0xffffffff',
}

tester_params = {
    'test_desc': 'Boot to ESXI 8.0.1 (debug image).',
    'os_build_type': 'debug',
    'os_version': 'U2-EA2-11372496',
    'networking:create_network': True,
    'networking:i82599_present': True,
    'ESXI_VERSION_STR': '8.0.2',
}

presets = [[ "./tests/perf/../common/dimms_1s_ucc_16x256GB.preset.yml" ]]

with env.Config(test_dir=simenv.log_dir, test_target=simenv.target, presets=presets, exec_timeout=3600) as test:
    create.run_target(simenv.target, platf_params, presets=presets)
    test.init_done()
    conf.boot_tester.enable_sie_check = False # to improve performance
    #cli.run_command('sim->fail_on_warnings = FALSE')
    cli.run_command('set-image-memory-limit (100*1024) "/tmp"')  
    #simenv.vtune = True
    cli.run_command(f'run-command-file {simenv.log_dir}/../../../../common/boot_profiling.include')
    conf.boot_tester.iface.tester.boot_test(conf.boot_tester.iface.tester.get_exec_mode('ESXI_DEBUG_MODE'), conf.boot_tester.iface.tester.get_scenario('SIMPLEBOOT'))
