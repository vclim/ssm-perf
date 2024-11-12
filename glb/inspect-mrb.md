# Simulated Cores

┌─────────────────────────────┬─┬─────────────────────────────┬──────────┬──────────────┬─────────┐
│          CPU Name           │ │          CPU Class          │   Freq   │     Cell     │Scheduled│
├─────────────────────────────┼─┼─────────────────────────────┼──────────┼──────────────┼─────────┤
│board.bmc.armcortexa7.core[0]│ │arm-cortex-a7                │  1.20 GHz│board.cell    │no       │
│board.bmc.armcortexa7.core[1]│ │arm-cortex-a7                │  1.20 GHz│board.cell    │no       │
│board.slk.lx7[0].cpu         │*│xtensa_control_slk_v1p2_core0│400.00 MHz│board.slk.cell│yes      │
│board.slk.lx7[1].cpu         │ │xtensa_control_slk_v1p2_core1│400.00 MHz│board.slk.cell│yes      │
└─────────────────────────────┴─┴─────────────────────────────┴──────────┴──────────────┴─────────┘
* = selected CPU


┌─────────────────────────────┬─────┬──────┬────────┐
│          Processor          │Steps│Cycles│Time (s)│
├─────────────────────────────┼─────┼──────┼────────┤
│board.bmc.armcortexa7.core[0]│    0│     0│   0.000│
│board.bmc.armcortexa7.core[1]│    0│     0│   0.000│
│board.slk.lx7[0].cpu         │    0│     0│   0.000│
│board.slk.lx7[1].cpu         │    0│     0│   0.000│
│ethernet_switch_mgmt.clock   │n/a  │     0│   0.000│
└─────────────────────────────┴─────┴──────┴────────┘

# Cells and Thread Domains

┌──────────┬──────┬─────────────────────────────┐
│   Cell   │Domain│           Objects           │
├──────────┼──────┼─────────────────────────────┤
│board.cell│    #0│board.bmc.armcortexa7.core[0]│
│          │      │board.bmc.armcortexa7.core[1]│
│          │      │board.cell                   │
└──────────┴──────┴─────────────────────────────┘
┌──────────────┬──────┬────────────────────┐
│     Cell     │Domain│      Objects       │
├──────────────┼──────┼────────────────────┤
│board.slk.cell│    #0│board.slk.cell      │
│              │      │board.slk.lx7[0].cpu│
│              │      │board.slk.lx7[1].cpu│
└──────────────┴──────┴────────────────────┘
┌─────────────┬──────┬──────────────────────────┐
│    Cell     │Domain│         Objects          │
├─────────────┼──────┼──────────────────────────┤
│default_cell0│    #0│default_cell0             │
│             │      │ethernet_switch_mgmt.clock│
└─────────────┴──────┴──────────────────────────┘

# Time Quantum and Min Latency

┌──────────────┬──────────┬───┬────────────┬─────────────┬───────────┐
│     cell     │   mode   │#td│time-quantum│max-time-span│min-latency│
├──────────────┼──────────┼───┼────────────┼─────────────┼───────────┤
│board.cell    │   n/a    │  0│(833.333 ns)│ (833.333 ns)│    10.0 ms│
│board.slk.cell│serialized│  1│      2.5 µs│     (2.5 µs)│    10.0 ms│
│default_cell0 │serialized│  1│    (1.0 ms)│     (1.0 ms)│    10.0 ms│
└──────────────┴──────────┴───┴────────────┴─────────────┴───────────┘

# Loaded Images

┌──────────────────────┬───────┬────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│Image                 │   Size│Unsaved data│File(s) (read-only/read-write)                                                                                │
├──────────────────────┼───────┼────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│board.bmc.spi_image0  │256 MiB│          no│/nfs/site/disks/simcloud_suihaich_001/personal.suihaich.simics-work/glb/targets/slk-soc/images/bmc_fw.bin (ro)│
│board.spi_flash._image│  8 GiB│          no│                                                                                                              │
└──────────────────────┴───────┴────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

# Packages

b>Simics Base (linux64) on Linux (5.14.21-150400.24.116-default)/b>

b>Installed Packages:/b>
┌────┬───────────┬────────────┬───────────────────────┐
│Pkg │   Name    │  Version   │       Build ID        │
├────┼───────────┼────────────┼───────────────────────┤
│1000│Simics-Base│7.17.0      │                   7031│
│2014│GilaBend   │7.0.0-pre.20│intel.ptac-stc:70240826│
└────┴───────────┴────────────┴───────────────────────┘

VMP kernel module: 1.16.5


# Ethernet Switch for Data

Status of ethernet_switch_data [class ethernet_switch]
======================================================

Setup:
         Top component : none
          Instantiated : True

Attributes:
             global_id : none
          goal_latency : 1e-05
    immediate_delivery : False

Connections:

# Ethernet Switch for Management

Cannot get status for ethernet_switch_mgmt

# Model Structure

┐
├ board ┐
│       ├ adk 
│       ├ bmc ┐
│       │     ├ RST_BMC_EXTRST_N_FROM_PFR 
│       │     ├ RST_SRST_BMC_N_FROM_PFR 
│       │     ├ adc1 
│       │     ├ adc2 
│       │     ├ ahbc 
│       │     ├ armcortexa7 ┐
│       │     │             ├ core[0] ┐
│       │     │             │         └ dbg 
│       │     │             ├ core[1] ┐
│       │     │             │         └ dbg 
│       │     │             ├ cp14 
│       │     │             ├ cpu_group 
│       │     │             ├ cpu_mem[0..1] 
│       │     │             ├ gic 
│       │     │             ├ gic_mem[0..1] 
│       │     │             ├ gic_mem_ns[0..1] 
│       │     │             ├ phys_mem 
│       │     │             ├ timer[0..1] 
│       │     │             └ unmapped_memory 
│       │     ├ bmc_io_space 
│       │     ├ boot_rom 
│       │     ├ boot_rom_image 
│       │     ├ com[0..4] 
│       │     ├ dram 
│       │     ├ emmc 
│       │     ├ espi 
│       │     ├ eth_slot0 
│       │     ├ eth_slot1 
│       │     ├ flash_image_space 
│       │     ├ fmc 
│       │     ├ gpio 
│       │     ├ hace 
│       │     ├ host_signal_handler 
│       │     ├ i2c 
│       │     ├ i2c_eeprom_0 
│       │     ├ i2c_eeprom_1 
│       │     ├ i2c_eeprom_2 
│       │     ├ i2c_eeprom_3 
│       │     ├ i2c_eeprom_ep_0 
│       │     ├ i2c_eeprom_ep_1 
│       │     ├ i2c_eeprom_ep_2 
│       │     ├ i2c_eeprom_ep_3 
│       │     ├ i2c_ep[0..15] 
│       │     ├ i2c_link[0..15] 
│       │     ├ i3c[0..5] 
│       │     ├ i3c_dbg 
│       │     ├ i3c_dbg_ep[0..5] 
│       │     ├ i3c_dbg_link[0..5] 
│       │     ├ i3c_link[0..5] 
│       │     ├ i3c_master_ep[0..5] 
│       │     ├ lpc 
│       │     ├ mac[0..3] 
│       │     ├ mac_phy[0..3] 
│       │     ├ mctp 
│       │     ├ mctp_rc 
│       │     ├ mii_bus[0..3] 
│       │     ├ mmbi 
│       │     ├ mmc 
│       │     ├ pcie ┐
│       │     │      ├ bridge ┐
│       │     │      │        └ downstream_port ┐
│       │     │      │                          ├ cfg_space 
│       │     │      │                          ├ io_space 
│       │     │      │                          ├ mem_space 
│       │     │      │                          └ msg_space 
│       │     │      ├ pci_vga 
│       │     │      ├ pcie_socket 
│       │     │      └ unmapped_memory 
│       │     ├ pcie_host 
│       │     ├ peci 
│       │     ├ pwm 
│       │     ├ rtc 
│       │     ├ scu 
│       │     ├ sdhc 
│       │     ├ sdram_image 
│       │     ├ sec 
│       │     ├ serial[0..4] 
│       │     ├ sio 
│       │     ├ socket 
│       │     ├ spi1 
│       │     ├ spi2 
│       │     ├ spi_flash_obj0 
│       │     ├ spi_image0 
│       │     ├ spi_rom 
│       │     ├ sram 
│       │     ├ sram_image 
│       │     ├ tmc 
│       │     ├ udma 
│       │     ├ uhci 
│       │     ├ unmapped_memory 
│       │     ├ usb_hub 
│       │     ├ ve 
│       │     ├ vuart 
│       │     └ wdt 
│       ├ cell ┐
│       │      └ ps 
│       ├ cell_context 
│       ├ i3c_bus 
│       ├ i3c_device 
│       ├ power_signal_bus 
│       ├ slk ┐
│       │     ├ cell ┐
│       │     │      └ ps 
│       │     ├ cell_context 
│       │     ├ console0 ┐
│       │     │          └ con ┐
│       │     │                ├ connector 
│       │     │                ├ frontend 
│       │     │                ├ recorder 
│       │     │                ├ tcp 
│       │     │                └ unix_socket 
│       │     ├ eth0 
│       │     ├ eth_br[0] ┐
│       │     │           └ offload ┐
│       │     │                     └ mem 
│       │     ├ eth_br[1] ┐
│       │     │           └ offload ┐
│       │     │                     └ mem 
│       │     ├ eth_br[2] ┐
│       │     │           └ offload ┐
│       │     │                     └ mem 
│       │     ├ eth_br[3] ┐
│       │     │           └ offload ┐
│       │     │                     └ mem 
│       │     ├ eth_br[4] ┐
│       │     │           └ offload ┐
│       │     │                     └ mem 
│       │     ├ eth_br[5] ┐
│       │     │           └ offload ┐
│       │     │                     └ mem 
│       │     ├ eth_br[6] ┐
│       │     │           └ offload ┐
│       │     │                     └ mem 
│       │     ├ eth_br[7] ┐
│       │     │           └ offload ┐
│       │     │                     └ mem 
│       │     ├ eth_br[8] ┐
│       │     │           └ offload ┐
│       │     │                     └ mem 
│       │     ├ eth_br[9] ┐
│       │     │           └ offload ┐
│       │     │                     └ mem 
│       │     ├ eth_br[10] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[11] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[12] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[13] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[14] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[15] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[16] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[17] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[18] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[19] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[20] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[21] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[22] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_br[23] ┐
│       │     │            └ offload ┐
│       │     │                      └ mem 
│       │     ├ eth_ss[0] ┐
│       │     │           ├ eth 
│       │     │           ├ mac ┐
│       │     │           │     └ mem 
│       │     │           └ phy ┐
│       │     │                 └ mem 
│       │     ├ eth_ss[1] ┐
│       │     │           ├ eth 
│       │     │           ├ mac ┐
│       │     │           │     └ mem 
│       │     │           └ phy ┐
│       │     │                 └ mem 
│       │     ├ eth_ss[2] ┐
│       │     │           ├ eth 
│       │     │           ├ mac ┐
│       │     │           │     └ mem 
│       │     │           └ phy ┐
│       │     │                 └ mem 
│       │     ├ eth_ss[3] ┐
│       │     │           ├ eth 
│       │     │           ├ mac ┐
│       │     │           │     └ mem 
│       │     │           └ phy ┐
│       │     │                 └ mem 
│       │     ├ eth_ss[4] ┐
│       │     │           ├ eth 
│       │     │           ├ mac ┐
│       │     │           │     └ mem 
│       │     │           └ phy ┐
│       │     │                 └ mem 
│       │     ├ eth_ss[5] ┐
│       │     │           ├ eth 
│       │     │           ├ mac ┐
│       │     │           │     └ mem 
│       │     │           └ phy ┐
│       │     │                 └ mem 
│       │     ├ eth_ss[6] ┐
│       │     │           ├ eth 
│       │     │           ├ mac ┐
│       │     │           │     └ mem 
│       │     │           └ phy ┐
│       │     │                 └ mem 
│       │     ├ eth_ss[7] ┐
│       │     │           ├ eth 
│       │     │           ├ mac ┐
│       │     │           │     └ mem 
│       │     │           └ phy ┐
│       │     │                 └ mem 
│       │     ├ eth_ss[8] ┐
│       │     │           ├ eth 
│       │     │           ├ mac ┐
│       │     │           │     └ mem 
│       │     │           └ phy ┐
│       │     │                 └ mem 
│       │     ├ eth_ss[9] ┐
│       │     │           ├ eth 
│       │     │           ├ mac ┐
│       │     │           │     └ mem 
│       │     │           └ phy ┐
│       │     │                 └ mem 
│       │     ├ eth_ss[10] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[11] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[12] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[13] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[14] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[15] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[16] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[17] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[18] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[19] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[20] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[21] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[22] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ eth_ss[23] ┐
│       │     │            ├ eth 
│       │     │            ├ mac ┐
│       │     │            │     └ mem 
│       │     │            └ phy ┐
│       │     │                  └ mem 
│       │     ├ iopic_eth_bridge 
│       │     ├ iopic_eth_ss 
│       │     ├ iopic_noc_ss 
│       │     ├ iopic_xsr_bridge 
│       │     ├ iopic_xsr_ss 
│       │     ├ irqbus ┐
│       │     │        └ EXTIRQ[0..15] 
│       │     ├ lx7[0] ┐
│       │     │        ├ cpu ┐
│       │     │        │     └ dbg 
│       │     │        ├ cpu_mem 
│       │     │        ├ dram ┐
│       │     │        │      └ _image 
│       │     │        ├ drom ┐
│       │     │        │      └ _image 
│       │     │        ├ eri_mem 
│       │     │        ├ idma 
│       │     │        ├ iram ┐
│       │     │        │      └ _image 
│       │     │        └ irom ┐
│       │     │               └ _image 
│       │     ├ lx7[1] ┐
│       │     │        ├ cpu ┐
│       │     │        │     └ dbg 
│       │     │        ├ cpu_mem 
│       │     │        ├ dram ┐
│       │     │        │      └ _image 
│       │     │        ├ eri_mem 
│       │     │        ├ idma 
│       │     │        └ iram ┐
│       │     │               └ _image 
│       │     ├ mac0 
│       │     ├ peripherals ┐
│       │     │             ├ ccupmu 
│       │     │             ├ dma ┐
│       │     │             │     └ endian[0..1] 
│       │     │             ├ i3c 
│       │     │             ├ sensors 
│       │     │             ├ spi 
│       │     │             └ uart 
│       │     ├ phy0 
│       │     ├ phys_mem 
│       │     ├ power_signal_bus 
│       │     ├ router 
│       │     ├ smem ┐
│       │     │      └ _image 
│       │     ├ tie_mailbox ┐
│       │     │             ├ fifo_0to1 
│       │     │             └ fifo_1to0 
│       │     ├ xsr_br[0..63] 
│       │     ├ xsr_ctrl[0..7] 
│       │     └ xsr_phy[0..63] 
│       └ spi_flash ┐
│                   └ _image 
├ bp ┐
│    ├ bank 
│    ├ console_string 
│    ├ control_register 
│    ├ cycle 
│    ├ cycle_event 
│    ├ exception 
│    ├ gfx 
│    ├ hap 
│    ├ log 
│    ├ magic 
│    ├ memory 
│    ├ notifier 
│    ├ os_awareness 
│    ├ source_line 
│    ├ source_location 
│    ├ step 
│    ├ step_event 
│    └ time 
├ default_cell0 ┐
│               └ ps 
├ default_cell0_context 
├ default_cell0_rec0 
├ default_sync_domain 
├ ethernet_switch_data ┐
│                      ├ device0 
│                      ├ ep8cb060e9e31b9c07 
│                      └ link 
├ ethernet_switch_mgmt ┐
│                      ├ clock 
│                      ├ device0 
│                      ├ device1 
│                      ├ device2 
│                      ├ ep2423886210a373a1 
│                      ├ ep669e187a3e63f50d 
│                      ├ epfe9c7e4d317aeca1 
│                      ├ link 
│                      └ sn ┐
│                           ├ connector_link0 
│                           ├ ftp 
│                           ├ ftp_c 
│                           ├ ftp_d 
│                           ├ sn 
│                           └ snd[0] 
├ params 
├ prefs 
├ sim ┐
│     ├ cli 
│     ├ gui 
│     ├ tlmtry 
│     └ transactions 
└ tcf 


