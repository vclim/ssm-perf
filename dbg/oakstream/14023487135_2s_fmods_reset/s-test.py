from simmod.pylib import create
from simmod.srv_tests import env


platf_params = {
    'init_testers': True,
    'log_dir': env.get_script_dir(),
    'os_type': 'uefi',
    'ifwi_product_type': 'consumer',
    'os_product_type': 'consumer',
    'ifwi_build_type': ['release'],
    'test_desc': 'Cold Reset from UEFI shell with Cf9 write.',
}

tester_params = {

}

test_target = "targets/oakstream/2_socket_ucc-aunit-cbbpunit-ese-imhpunit-oobmsm-s3m.target.yml"
presets = [['presets/perf_profile_fast']]

with env.Config(test_dir=env.get_script_dir(), test_target=test_target, presets=presets, exec_timeout=3600) as test:
    create.run_target(test_target, platf_params, presets=presets)
    test.init_done()
    conf.reset_tester.enable_sie_check = False 
    conf.reset_tester.iface.tester.reset_test( conf.reset_tester.iface.tester.get_exec_mode('UEFI_MODE'), conf.reset_tester.iface.tester.get_reset_mode('COLD_RESET'))
