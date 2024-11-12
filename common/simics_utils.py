import time
import datetime
import simics
import cli
import sys
import os
import timeit
import cProfile
import pstats

class SimPoint:
    def __init__(self, primary_core: str = None):
        if primary_core is not None:
            self.primary_core = primary_core
        else:
            self.primary_core = simics.SIM_get_all_processors()[0].name

        self.rtime = time.time()

        # process 'ptime -all' output
        tmp, self.ptime_output = cli.quiet_run_command('ptime -all')
        self.vtimes = {}
        self.instr_counts = {}
        self.cycle_counts = {}
        for val in tmp:
            self.instr_counts.update({val[0]: val[1]})
            self.cycle_counts.update({val[0]: val[2]})
            self.vtimes.update({val[0]: val[3]})

        # Note: class IO_stat_cmds (applications.simulators.simics.simics-base/core/src/core/common/commands.py)
        # tracks io stats and step counts inside the class, and will clear all of them when clear-io-stats is called.
        # This will not affect the "ptime" output which gets the steps/cycles from cpu object
        # (see print_time_cmd in applications.simulators.simics.simics-base/core/src/core/common/proc_commands.py)
        #
        # We'll calculate the difference between io-stats output in the print_delta method,
        # so there's no need to manually calling clear-io-stats.
        # The device accesses statistics will reflect the window from the beginning of the simulation, instead of the elapsed window.

        # process 'io-stats' output
        self.io_stats_output = cli.quiet_run_command('io-stats')[1]
        tmp = self.io_stats_output.split('\n')
        self.io_count = int( tmp[0].split()[3] )
        if len(tmp)>1 and tmp[1]:
            self.total_step_count = int( tmp[1].split()[3] )
        else:
            self.total_step_count = 0
        if len(tmp)>2:
            self.total_step_count_non_idle = int( tmp[2].split()[3] )
        else:
            self.total_step_count_non_idle = 0
        if len(tmp)>3:
            self.dev_access_stats = "\n".join(tmp[3:])
        else:
            self.dev_access_stats = ""

    def print_delta(self, simpoint, msg=""):
        print(f'\n=============================')
        print(f'[{msg}] Elapsed time (in minutes)         = {((self.rtime - simpoint.rtime)/60):.2f}')
        print(f'[{msg}] Elapsed virtual time (in seconds) = {(self.vtimes[self.primary_core] - simpoint.vtimes[self.primary_core]):.3f}')
        print(f'[{msg}] Primary core                      = {self.primary_core}\n')
        print(f'[{msg}] Elapsed total step count (may include idle steps) = {(self.total_step_count - simpoint.total_step_count):,d}')
        print(f'[{msg}] Elapsed total step count (excluding idle steps)   = {(self.total_step_count_non_idle - simpoint.total_step_count_non_idle):,d}')
        print(f'[{msg}] Elapsed total IO accesses                         = {(self.io_count - simpoint.io_count):,d}')
        print(f'[{msg}] IO access rate (per sec in virtual time)          = {((self.io_count - simpoint.io_count)/(self.vtimes[self.primary_core] - simpoint.vtimes[self.primary_core])):,.1f}')
        print(f'[{msg}] Average steps (excluding idle steps) per IO       = {((self.total_step_count_non_idle - simpoint.total_step_count_non_idle)//self.io_count):,d}')
        print(f'[{msg}] MIPS (excluding idle steps)                       = {((self.total_step_count_non_idle - simpoint.total_step_count_non_idle)/(self.rtime - simpoint.rtime)/1000000):,.3f}')
        print(f'[{msg}] Simulated MIPS (excluding idle steps)             = {((self.total_step_count_non_idle - simpoint.total_step_count_non_idle)/(self.vtimes[self.primary_core] - simpoint.vtimes[self.primary_core])/1000000):,.3f}')
        print(f'[{msg}] Slowdown factor (real/virtual time)               = {((self.rtime - simpoint.rtime)/(self.vtimes[self.primary_core] - simpoint.vtimes[self.primary_core])):,.1f}')
        print(f'\n[{msg}] Device access stat (from start of simulation):')
        print(self.dev_access_stats)
        print(f'\n[{msg}] Elapsed step count for all cores (may include idle steps):')
        for c in sorted(self.instr_counts.keys()):
            print(f'[{msg}] {c} : {(self.instr_counts[c] - simpoint.instr_counts[c]):,d}')
        print(f'=============================\n')

# WARNING: the sampled activity state may not be representative for the entire interval
class X86CoreActivityState:
    def __init__(self, cores, interval=0.1):
        self.cores = [simics.SIM_get_object(name) for name in cores]
        self.interval = interval
        self.num_samples = 0
        self.batch = 100000
        self.num_states = 7
        self.history = [ [None]*self.batch for _ in range(len(self.cores)) ]

    def update(self):
        for (i, c) in enumerate(self.cores):
            if self.num_samples>0.99*len(self.history[0]):
                self.history[i].extend([None]*self.batch)
            self.history[i][self.num_samples] = c.activity_state
        self.num_samples += 1

    def clear(self):
        self.num_samples = 0
        self.history = [ [ None for _ in range(self.batch) ] for _ in range(len(self.cores)) ]

    def calc_percentage(self):
        tmp = [ [ -1 for _ in range(self.num_states) ] for _ in range(len(self.cores)) ]
        for (i, c) in enumerate(self.cores):
            for s in range(self.num_states):
                tmp[i][s] = int( self.history[i].count(s) / self.num_samples * 100 )
        return tmp

    def report(self):
        # The decoding of the activity state value (from [x86_processor_class.h](https://github.com/intel-innersource/applications.simulators.simics.simics-base/blob/7/src/cpu/x86/x86_processor_class.h)):
        print('PERF: print x86 core activity state statistics')
        stat = self.calc_percentage()
        print(f'|{" "*len(self.cores[0].name)} |    EXE |    HLT |    OFF | W4SIPI |     CX |  MWAIT | SENTER_SLEEP |')
        for (i, c) in enumerate(self.cores):
            print(f'|{c.name} | {stat[i][0]:6d} | {stat[i][1]:6d} | {stat[i][2]:6d} | {stat[i][3]:6d} | {stat[i][4]:6d} | {stat[i][5]:6d} | {stat[i][6]:12d} |')

    def report_and_clear(self):
        self.report()
        self.clear()

class Probes:

    global_level1 = [ ("sim.time.virtual", "current"), "sim.slowdown", "sim.time.schedule", "sim.esteps", "sim.mips", "sim.load_percent", "sim.io_access_count", "sim.process.cpu_percent", "sim.process.cpu_usage_percent" ]

    global_level2 = [ ("sim.time.virtual", "current"), "sim.attribute.reads", "sim.attribute.writes", "sim.event.step.intensity", "sim.interface.lookups", "sim.exec_mode.vmp_steps", "sim.exec_mode.vmp_percent" ]

    # sim.event.cycle.intensity may cause up to 50% overhead in 2S max core config
    global_level3 = [ ("sim.time.virtual", "current"), "sim.event.cycle.intensity" ]

    core_level1 = [ ("sim.time.virtual", "current"), "cpu.esteps", "cpu.load_percent", "cpu.instructions_per_cycle", "cpu.schedule_percent", "cpu.time.schedule", "cpu.mips", "cpu.exec_mode.hypersim_percent", "cpu.exec_mode.interpreter_percent", "cpu.exec_mode.jit_percent", "cpu.exec_mode.vmp_percent"]

    # WARNING: the sampled value may not be representative for the entire interval when mode=current, esteps should be used as an indicator of how busy/idle is the core
    core_disabled_reason = [ ("sim.time.virtual", "current"), ("cpu.disabled_reason", "current") ]

    host_mem_usage = [ ("sim.time.virtual", "current"), ("host.memory.used", "current") ]

    fmod_sum = [ "cpu.time.schedule", "cpu.esteps" ]
    bmod_sum = [ "cpu.time.schedule", "cpu.esteps" ]

    @classmethod
    def create_fmod_sum_probes(cls, probe_list, num_cpus=1):
        results = []
        for probe in probe_list:
            for socket in range(num_cpus):
                groups = dict()
                groups['x86']   = [ x.name for x in simics.SIM_get_all_processors() if f'mcp{socket}' in x.name and x.classname=='x86-panther-cove' ]
                groups['s3m']   = [ x.name for x in simics.SIM_get_all_processors() if f's3m{socket}' in x.name and x.classname=='arcsem110' ]
                groups['msm']   = [ x.name for x in simics.SIM_get_all_processors() if f'mcp{socket}' in x.name and x.classname=='xtensa_OOBMSM_Tie_v8_DMR' ]
                groups['ese']   = [ x.name for x in simics.SIM_get_all_processors() if f'mcp{socket}' in x.name and x.classname=='x86-lmt-cse4-cet' ]
                groups['aunit'] = [ x.name for x in simics.SIM_get_all_processors() if f'mcp{socket}' in x.name and x.classname=='xtensa_pnc_pm_xt_1_1' ]
                groups['punit'] = [ x.name for x in simics.SIM_get_all_processors() if f'mcp{socket}' in x.name and (x.classname=='xtensa_srvr_xtensa_v002_22ww44_1' or x.classname=='xtensa_dmr_uc_rtltie_23ww11') ]
                for k,v in groups.items():
                    sum_probe_name = f'socket{socket}_{probe.replace(".","_")}_{k}'
                    results.append(sum_probe_name)
                    tmp = str(v).replace("'", '"') # replace single quote with double quote after converting list of obj names to string
                    cli.run_command(f'probes.new-sum-probe probe = {probe} name = {sum_probe_name} objects = {tmp}')
                    print(f'PERF: created sum probe {sum_probe_name} which is a sum of {probe} for following {len(v)} objects:')
                    for x in v:
                        print(f'    {x}')
        return results

    @classmethod
    def create_bmod_sum_probes(cls, probe_list, num_cpus=1):
        results = []
        for probe in probe_list:
            for socket in range(num_cpus):
                groups = dict()
                groups['bsp'] = [ x.name for x in simics.SIM_get_all_processors() if f'mcp{socket}' in x.name and 'cbb_die0.tile0.module0.core[0][0]' in x.name ]
                groups['asp'] = [ x.name for x in simics.SIM_get_all_processors() if f'mcp{socket}' in x.name and 'cbb_die0.tile0.module0.core[0][0]' not in x.name ]
                for k,v in groups.items():
                    sum_probe_name = f'socket{socket}_{probe.replace(".","_")}_{k}'
                    results.append(sum_probe_name)
                    tmp = str(v).replace("'", '"') # replace single quote with double quote after converting list of obj names to string
                    cli.run_command(f'probes.new-sum-probe probe = {probe} name = {sum_probe_name} objects = {tmp}')
                    print(f'PERF: created sum probe {sum_probe_name} which is a sum of {probe} for following {len(v)} objects:')
                    for x in v:
                        print(f'    {x}')
        return results


def set_processors_attr(attr, val):
    print(f'[simics_utils] setting {attr} in all processors to {val}')
    for obj in simics.SIM_get_all_processors():
        try:
            setattr(obj, attr, val)
        except:
            print(f'[simics_utils] failed to set attribute {attr} for {obj}')

def print_processors_attr(attr, format=''):
    print(f'[simics_utils] printing {attr} in all processors:')
    for obj in simics.SIM_get_all_processors():
        try:
            if format=='hex':
                print(f'{obj.name} : {hex(getattr(obj, attr))}')
            else:
                print(f'{obj.name} : {getattr(obj, attr)}')
        except:
            pass

def print_vmp_stats(run_enable_feature_cmd=False, clear=False):
    # we wrap vmp-stats in python try-except because simics try-except doesn't catch some errors
    if run_enable_feature_cmd:
        cli.run_command('enable-unsupported-feature internals')
    try:
        cli.run_command('vmp-stats')
    except Exception as e:
        print(f'[WARNING] cannot print vmp stats: {e}')
    if clear:
        try:
            cli.run_command('vmp-stats-clear')
        except Exception as e:
            print(f'[WARNING] cannot clear vmp stats: {e}')

def vtune_start(name='vtune0'):
    os.environ['PATH'] += ':/nfs/site/disks/central_tools_tree/sles12/flamegraph/FlameGraph/'
    cli.run_command('enable-unsupported-feature feature = vtune-measurement -v')
    cli.run_command(f'new-vtune-measurement {name} vtune-path=/nfs/site/disks/central_tools_tree/sles12/vtune/2022.1.0/bin64')
    cli.run_command(f'{name}.start')
    print(f'PERF: vtune {name} started')

def vtune_stop(name='vtune0', svg='vtune.svg', profile='vtune_hotspots.csv'):
    cli.run_command(f'{name}.stop')
    cli.run_command(f'{name}.flamegraph svg-output-filename={svg}')
    print(f'PERF: vtune {name} stopped and svg file saved to {svg}')
    cli.run_command(f'{name}.summary')
    cli.run_command(f'{name}.thread-profile')
    cli.run_command(f'{name}.module-profile')
    cli.run_command(f'{name}.profile')
    # get result path from summary output, the first line always in the form of - vtune: Using result path `...'
    result_path = cli.quiet_run_command(f'{name}.summary')[1].split('\n')[0][26:-1]
    os.system(f'/nfs/site/disks/central_tools_tree/sles12/vtune/2022.1.0/bin64/vtune -R hotspots -call-stack-mode all -report-output {profile} -format csv -csv-delimiter comma -r {result_path}')

def vtune_profile(name='vtune0', svg='vtune.svg', profile='vtune_hotspots.csv', start=0, end=0):
    if end<=start:
        cli.run_command(f'interrupt-script "simics_utils:vtune_profile - end time ({end}) has to be greater than start time ({start})" -error')
    else:
        if start>0:
            cli.run_command('script-branch { ' + f'wait-for-global-time {start}; `simics_utils.vtune_start("{name}")`; wait-for-global-time {end}; `simics_utils.vtune_stop("{name}", "{svg}", "{profile}")`' + ' }')
        else:
            cli.run_command('script-branch { ' + f'`simics_utils.vtune_start("{name}")`; wait-for-global-time {end}; `simics_utils.vtune_stop("{name}", "{svg}", "{profile}")`' + ' }')

def timeit_simics_cmd(cmd):
    print("PERF (" + cmd + "): " + str(timeit.timeit(f'import cli; cli.run_command(\'{cmd}\')', number=1)))

def cprofile_simics_cmd(cmd):
    cProfile.run(f'cli.run_command(\'{cmd}\')', 'cprofile.dump')
    p=pstats.Stats('cprofile.dump')
    return p

class ProbeMon:
    def __init__(self, name, sampling_mode="virtual", interval=1, clock="", output=""):
        #print(f'[simics_utils] Creating probe monitor {name} (sampling-mode = {sampling_mode} interval = {interval} clock = {clock} output-file = {output}')
        self.name, self.sampling_mode, self.interval = name, sampling_mode, interval
        cmd = f'new-probe-monitor name = {name} sampling-mode = {sampling_mode} interval = {interval} -print-no-samples'
        if clock:
            self.clock = clock
            cmd += f' clock = {clock}'
        if output:
            self.output = output
            cmd += f' output-file = {output}'
        cli.run_command(cmd)

    def add_probes(self, probe_list):
        for probe in probe_list:
            if type(probe)==tuple:
                # mode is specified
                print(f'[simics_utils] Adding {probe[0]} (mode={probe[1]})')
                cli.run_command(f'{self.name}.add-probe {probe[0]} mode = {probe[1]}')
            else:
                # mode is unspecified (default is delta)
                print(f'[simics_utils] Adding {probe} (mode=delta)')
                cli.run_command(f'{self.name}.add-probe {probe}')

def simics_setting_check(core_class='x86-glc', nic_class='i82599_comp', core_substr='egs01'):
    # simics.github\egs\simics_setting_check.py
    def get_IPC(t3):
        return f'{t3[0]}/{t3[1]}'
    def check(array, name, expected=None):
        if len(array)==0:
            print(f'WARNING: {name} is not set')
            return
        dedup = list(set(array))
        try:
            if len(dedup)==1:
                if expected!=None:
                    if dedup[0]!=expected:
                        print(f'WARNING: value of {name} is not expected (actual={dedup[0]}, expected={expected})')
                    else:
                        print(f'INFO: value of {name} is expected ({dedup[0]})')
                else:
                    # just check for consistency and print out the value as FYI
                    print(f'INFO: {name} = {dedup[0]}')
            else:
                print(f'WARNING: inconsistency found in values for {name} (unique values are {dedup})')
        except:
            print(f'WARNING: failed to check {name} ({array}')

    print('=== check simics settings starts ===')
    all_cores = [ obj for obj in SIM_get_all_objects() if obj.classname==core_class and (core_substr in obj.name if core_substr else True) ]
    all_nics  = [ obj for obj in SIM_get_all_objects() if obj.classname==nic_class]
    check([nic.pci_bus.destination[0]               for nic in all_nics],       'nic connection')
    check([core.freq_mhz                            for core in all_cores],     'core->freq_mhz')
    check([core.use_halt_steps                      for core in all_cores],     'core->use_halt_steps',                     False)
    check([core.cpuid_cet_ss_override               for core in all_cores],     'core->cpuid_cet_ss_override',              0)
    check([core.cpuid_cet_ibt_override              for core in all_cores],     'core->cpuid_cet_ibt_override',             0)
    check([core.cpuid_bus_lock_intercept_override   for core in all_cores],     'core->cpuid_bus_lock_intercept_override',  0)
    check([core.cpuid_la57_override                 for core in all_cores],     'core->cpuid_la57_override',                0)
    check([core.cpuid_physical_bits_override        for core in all_cores],     'core->cpuid_physical_bits_override',       46)
    check([core.cpuid_linaddr_width_override        for core in all_cores],     'core->cpuid_linaddr_width_override',       48)
    check([core.cpuid_lass_override                 for core in all_cores],     'core->cpuid_lass_override',                0)
    check([core.cpuid_has_avx512f_override          for core in all_cores],     'cpuid_has_avx512f_override',               0)
    check([core.cpuid_avx512_4fmaps_override        for core in all_cores],     'cpuid_avx512_4fmaps_override',             0)
    check([core.cpuid_avx512_4vnniw_override        for core in all_cores],     'cpuid_avx512_4vnniw_override',             0)
    check([core.cpuid_avx512_bf16_override          for core in all_cores],     'cpuid_avx512_bf16_override',               0)
    check([core.cpuid_avx512_bitalg_override        for core in all_cores],     'cpuid_avx512_bitalg_override',             0)
    check([core.cpuid_avx512_vbmi2_override         for core in all_cores],     'cpuid_avx512_vbmi2_override',              0)
    check([core.cpuid_avx512_vpopcntdq_override     for core in all_cores],     'cpuid_avx512_vpopcntdq_override',          0)
    check([core.cpuid_avx512bw_override             for core in all_cores],     'cpuid_avx512bw_override',                  0)
    check([core.cpuid_avx512cd_override             for core in all_cores],     'cpuid_avx512cd_override',                  0)
    check([core.cpuid_avx512dq_override             for core in all_cores],     'cpuid_avx512dq_override',                  0)
    check([core.cpuid_avx512er_override             for core in all_cores],     'cpuid_avx512er_override',                  0)
    check([core.cpuid_avx512fp16_override           for core in all_cores],     'cpuid_avx512fp16_override',                0)
    check([core.cpuid_avx512ifma_override           for core in all_cores],     'cpuid_avx512ifma_override',                0)
    check([core.cpuid_avx512pf_override             for core in all_cores],     'cpuid_avx512pf_override',                  0)
    check([core.cpuid_avx512vbmi_override           for core in all_cores],     'cpuid_avx512vbmi_override',                0)
    check([core.cpuid_avx512vl_override             for core in all_cores],     'cpuid_avx512vl_override',                  0)
    check([core.cpuid_avx512vnni_override           for core in all_cores],     'cpuid_avx512vnni_override',                0)
    check([core.cpuid_avx512vp2intersect_override   for core in all_cores],     'cpuid_avx512vp2intersect_override',        0)
    check([core.cpuid_amx_bf16_override             for core in all_cores],     'cpuid_amx_bf16_override',                  0)
    check([core.cpuid_amx_int8_override             for core in all_cores],     'cpuid_amx_int8_override',                  0)
    check([core.cpuid_amx_tile_override             for core in all_cores],     'cpuid_amx_tile_override',                  0)
    check([core.cpuid_pks_override                  for core in all_cores],     'cpuid_pks_override',                       0)
    check([core.cpuid_pku_override                  for core in all_cores],     'cpuid_pku_override',                       0)
    check([core.cpuid_monitor_mwait_enabled_override for core in all_cores],    'cpuid_monitor_mwait_enabled_override',     0)
    check([core.msr_ia32_core_capabilities>>5 & 1   for core in all_cores if core.msr_ia32_core_capabilities!=None],      'core->msr_ia32_core_capabilities split lock bit (will be set after core reset)',0)
    check([core.cpuid_has_mpx_override              for core in all_cores if core.cpuid_has_mpx_override!=None],          'core->cpuid_has_mpx_override',             0)
    check([core.cpuid_xcr0_mask_lower_override>>3 & 3 for core in all_cores if core.cpuid_xcr0_mask_lower_override!=None],'core->cpuid_xcr0_mask_lower_override MPX bits [4:3]',     0)
    check([get_IPC(core.step_rate)                  for core in all_cores],     'IPC',                                      '1/1')

    try:
        check([conf.ethernet_switch0.link.immediate_delivery],                      'ethernet_switch0.link->immediate_delivery',False)
    except:
        print(f'WARNING: error in accessing ethernet_switch0.link->immediate_delivery')

    check([cli.quiet_run_command('set-min-latency')[1].strip()],                'min latency')
    check([cli.quiet_run_command('cpu-switch-time')[0]*1e6],                    'time quantum (in microseconds)')
    check([core.rdtsc_slow_cycles                   for core in all_cores],     'core->rdtsc_slow_cycles')

    cli.run_command('list-thread-domains')
    cli.run_command('set-thread-limit')
    cli.run_command('set-max-time-span')

    print('=== check simics settings ends ===')


def enable_cache_reads_for_images(ip=''):
    if ip:
        images = [x for x in simics.SIM_object_iterator(None) if x.classname=='image' and ip in x.name]
    else:
        images = [x for x in simics.SIM_object_iterator(None) if x.classname=='image']
    for obj in images:
        obj.cache_reads = True

#def set_cpu_feature():
#    for obj in simics.SIM_get_all_processors():
#        try:
#            # ia32_core_capabilities[5:4] (set to disable)
#            #obj.msr_ia32_core_capabilities |= 0x3
#
#            # msr_memory_ctrl_msr[29:28] (33H, set to disable)
#            #tmp = int( cli.quiet_run_command(f'{obj.name}.read-msr 0x33')[-1], 0)
#            #cli.run_command(f'{obj.name}.set-msr 0x33 {tmp|(3<<28)}')
#
#            # ia32_debugctl[2] (bus lock detection, set to detect)
#            #obj.ia32_debugctl &= ~(1<<2)
#
#            # IA32_VMX_PROCBASED_CTLS2[62] (vmm bus-lock detection)
#            obj.ia32_vmx_procbased_ctls2 &= ~(1<<62)
#
#        except Exception as e:
#        #    print('[ERROR] set_cpu_feature failed')
#            pass
#
#def check_cpu_feature():
#    print('cpuid_bus_lock_intercept_override (0) | cpuid_memory_ctrl_override (1) | ia32_core_capabilities[5:4] (set to disable) | msr_memory_ctrl_msr[29:28] (33H, set to disable) | ia32_debugctl[2] (bus lock detection, set to detect) | IA32_VMX_PROCBASED_CTLS2[62] (vmm bus-lock detection)')
#    for obj in simics.SIM_get_all_processors():
#        try:
#            tmp = cli.quiet_run_command(f'{obj.name}.read-msr 0x33')[-1]
#            tmp = (int(tmp, 0) >> 28 ) & 0x3
#            print(f'{obj.cpuid_bus_lock_intercept_override} | {obj.cpuid_memory_ctrl_override} | {((obj.msr_ia32_core_capabilities>>4)&0x3)} | {tmp} | {((obj.ia32_debugctl>>2)&0x1)} | {((obj.ia32_vmx_procbased_ctls2>>62)&0x1)}')
#        except Exception as e:
#            pass #print('[ERROR] check_cpu_feature failed')
#
#def log(line, test_start_time, *args):
#    system = SIM_get_object(simenv.system)
#    L = system.log_level
#    system.log_level = 1
#    virtual = SIM_time(SIM_get_object(simenv.system))
#    real = time.time() - test_start_time
#    times = "[v: %.2f, r: %.2f] " % (virtual, real)
#    SIM_log_info(1, system, 1, times + (line % args))
#    system.log_level = L


