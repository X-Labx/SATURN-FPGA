Follow the instuctions below to boot Linux on the Saturn board.

DISCLAIMER: There are no guarantees this will work for you. It is provided as is - and for reference, learning and for your own research purposes.

Generate a EDK project as per the tutorial in the PDF, an example project is also included in a the HW_PROJ_EDK.zip file.
Test the hardware by exporting to the SDK (xsdk) and building a Memory Test application. You will need to set the base address in the linker script to the DDR base address instead of BRAM, otherwise you will get a compile error.
-In xsdk, next program device with the bit file.
-Then select the app, right click -> Run-As -> Launch on Hardware (GDB)
-It will execute and write to the serial port at 115200 baud.


Next create a Hello World project in the SDK if the above was not followed, as a file from it is needed.
Copy SaturnV3Linux.xml (./saturnlinux/SDK/SDK_Export/hw) to a new directory (e.g. device_tree_create).
Copy system.mss (./saturnlinux/workspace/MemTests1_bsp) to the same directory.
Commands are below.
- cd ~
- mkdir device_tree_create
- cp ../saturnlinux/SDK/SDK_Export/hw/SaturnV3Linux.xml .
- cp ../saturnlinux/workspace/MemTests1_bsp/system.mss .
Run nano system.mss and replace the text block below with the text block after it.
 
BEGIN OS
 PARAMETER OS_NAME = standalone
 PARAMETER OS_VER = 3.11.a
 PARAMETER PROC_INSTANCE = microblaze_0
 PARAMETER STDIN = ft2232_uart
 PARAMETER STDOUT = ft2232_uart
END

BEGIN OS
 PARAMETER OS_NAME = device-tree
 PARAMETER OS_VER = 3.10.a
 PARAMETER PROC_INSTANCE = microblaze_0
 PARAMETER CONSOLE DEVICE = ft2232_uart
END

Now run mkdir bsp/device-tree_v3_10_a/data in the device_tree_create folder, ensure the directory was created correctly.
Extract the device-tree-files.zip files to the new folder, ensure the files are in the data folder and not a sub-folder.
It should look as follows on disk:
.\SaturnV3Linux.xml
.\system.mss
.\bsp\device-tree_v3_10_a\data\device-tree_v2_1_0.mld
.\bsp\device-tree_v3_10_a\data\device-tree_v2_1_0.tcl 

Next run libgen -hw SaturnV3Linux.xml -lp device-tree -pe microblaze_0 system.mss
This should output a new microblaze folder, go into ./microblaze_0/libsrc/device-tree_v3_10_a and you will find a xilinx.dts file.
Rename the file xilinx.dts to saturn_v3.dts

Open saturn_v3.dts in nano and replace the bootargs lines with the following
bootargs = "console=ttyUL0";
linux,stdout-path = "/axi@0/serial@40600000";

Make sure that the base address 40600000 in the above line matches with the base address of FT2232H UART base address in EDK.

From the top folder run: cp microblaze_0/libsrc/device-tree_v3_10_a/saturn_v3.dts . 
An example dts, is also in the device-tree-create.zip file, but it will not match your system more than likely.


Set up a build server (i.e., VPS) and ensure the correct packages are installed, see the tutorial PDFs. A Ubuntu VPS 18.04 should work.
Create a directory, change into it and get the buildroot-2017.02.10.tar.gz file and extract it, and run: cd buildroot-2017.02.10/ .
Now extract the files from buildroot-configfiles.zip into the corresponding folders in the buildroot directory. 

You can replace the dts file with the one created as they will likely differ (interrupt assignment for example), and may stop it booting properly.

Note, the above step as it may cause the boot to hang if the wrong dts is used.

In the buildroot-2017.02.10 folder run:
 make numato_saturn_v3_defconfig
This will create a .config file for buildroot.
Next to customise or inspect the config run:
 make nconfig
Then to make the binary and microblaze tools (built by buildroot as per the config) start a new Linux screen session, ensure you're in the correct folder then run make.
 screen
 pwd
 make
It will take a while to build the tools and kernel image from scratch so you can disconnect, etc.

Finally go into ./saturnLinuxBuild/buildroot-2017.02.10/output/images where there should be a file simpleImage.saturn_v3 which can be used on the FPGA if it has been complied against your dts file. 
Move it to the directory with the hardware project in, an example image is included in a zip file also.

Re-run xsdk in the saturn hardware directory, also copy the image to this directory. Now program the board with the bitstream and run the HelloWorld or MemTest app again.
Check everything runs. Now you need to use the XMD tool to communicate with the MicroBlaze. There are two ways to do this. In xsdk or from the command line.

-For in the sdk do Xilinx Tools->XMD console (this may not work with the later steps due to the way xsdk reads the project) e.g., download errors.
-The other way is to run XMD from the command line.
-You need the bit file already downloaded, do via xsdk or impact ( use ./workspace/saturnlinux_hw_platform/download.bit ).
-Download the image then boot the board which will output the Linux bring up via the serial port, commands:
xmd
connect mb mdm
dow simpleImage.saturn_v3
con 0xa4000000

xmd Output:
XMD% 
XMD% connect mb mdm

JTAG chain configuration
--------------------------------------------------
Device   ID Code        IR Length    Part Name
 1       44008093           6        XC6SLX45

MicroBlaze Processor Configuration :
-------------------------------------
Version............................8.50c
Optimization.......................Performance
Interconnect.......................AXI-LE
MMU Type...........................Full_MMU
No of PC Breakpoints...............1
No of Read Addr/Data Watchpoints...0
No of Write Addr/Data Watchpoints..0
Instruction Cache Support..........on
Instruction Cache Base Address.....0xa4000000
Instruction Cache High Address.....0xa7ffffff
Data Cache Support.................on
Data Cache Base Address............0xa4000000
Data Cache High Address............0xa7ffffff
Exceptions  Support................on
FPU  Support.......................off
Hard Divider Support...............on
Hard Multiplier Support............on - (Mul64)
Barrel Shifter Support.............on
MSR clr/set Instruction Support....on
Compare Instruction Support........on
PVR Supported......................on
PVR Configuration Type.............Full
Data Cache Write-back Support......off
Fault Tolerance Support............off
Stack Protection Support...........off

Connected to "mb" target. id = 0
Starting GDB server for "mb" target (id = 0) at TCP port no 1234
XMD% 
XMD% dow simpleImage.saturn_v3
Downloading Program -- simpleImage.saturn_v3
	section, .text: 0xc0000000-0xc02b1ca7
	section, .init.text: 0xc0389000-0xc03a62c7
	section, .init.ivt: 0xc03a7c68-0xc03a7c8f
	section, __fdt_blob: 0xc02b1ca8-0xc02b9ca7
	section, .rodata: 0xc02ba000-0xc035a03f
	section, __ksymtab: 0xc035a040-0xc035f09f
	section, __ksymtab_gpl: 0xc035f0a0-0xc0361687
	section, __ksymtab_strings: 0xc0361688-0xc0371c8a
	section, __param: 0xc0371c8c-0xc0371f5b
	section, __modver: 0xc0371f5c-0xc0371fff
	section, __ex_table: 0xc0372000-0xc037350f
	section, .notes: 0xc0373510-0xc0373533
	section, .sdata2: 0xc0373534-0xc0373fff
	section, .data: 0xc0374000-0xc038893f
	section, .init.data: 0xc03a62c8-0xc03a7c67
	section, .init.setup: 0xc03a7c90-0xc03a7f9b
	section, .initcall.init: 0xc03a7f9c-0xc03a81fb
	section, .con_initcall.init: 0xc03a81fc-0xc03a81ff
	section, .init.ramfs: 0xc03a8200-0xc0572d43
	section, .bss: 0xc0573000-0xc05a4d0b
Download Progress......10......20.....30......40.....50......60......70......80.....90......Done
Setting PC with Program Start Address 0xa4000000
System Reset .... DONE

XMD% con 0xa4000000
Processor started. Type "stop" to stop processor

Serial port output:
Early console on uartlite at 0x40600000
bootconsole [earlyser0] enabled
Ramdisk addr 0x800065a6, Compiled-in FDT at c02e4178
Linux version 4.9.13 (root@ubuntu-s-1vcpu-1gb-nyc3-01) (gcc version 5.4.0 (Buildroot 2017.02.10) ) #2 Wed Jun 23 15:44:39 UTC 2021
setup_cpuinfo: initialising
setup_cpuinfo: Using full CPU PVR support
ERROR: Microblaze BARREL, MSR, PCMP or DIV-different for kernel and DTS
ERROR: Microblaze HW_MUL-different for kernel and DTS
wt_msr_noirq
setup_memory: max_mapnr: 0x4000
setup_memory: min_low_pfn: 0xa4000
setup_memory: max_low_pfn: 0xa8000
setup_memory: max_pfn: 0xa8000
Zone ranges:
  DMA      [mem 0x00000000a4000000-0x00000000a7ffffff]
  Normal   empty
Movable zone start for each node
Early memory node ranges
  node   0: [mem 0x00000000a4000000-0x00000000a7ffffff]
Initmem setup node 0 [mem 0x00000000a4000000-0x00000000a7ffffff]
On node 0 totalpages: 16384
free_area_init_node: node 0, pgdat c03c9014, node_mem_map c04e1000
  DMA zone: 128 pages used for memmap
  DMA zone: 0 pages reserved
  DMA zone: 16384 pages, LIFO batch:3
early_printk_console remapping from 0x40600000 to 0xffffd000
pcpu-alloc: s0 r0 d32768 u32768 alloc=1*32768
pcpu-alloc: [0] 0
Built 1 zonelists in Zone order, mobility grouping on.  Total pages: 16256
Kernel command line: console=ttyUL0,115200
PID hash table entries: 256 (order: -2, 1024 bytes)
Dentry cache hash table entries: 8192 (order: 3, 32768 bytes)
Inode-cache hash table entries: 4096 (order: 2, 16384 bytes)
Memory: 59864K/65536K available (2960K kernel code, 98K rwdata, 776K rodata, 892K init, 210K bss, 5672K reserved, 0K cma-reserved)
Kernel virtual memory layout:
  * 0xffffe000..0xfffff000  : fixmap
  * 0xffffd000..0xffffe000  : early ioremap
  * 0xf0000000..0xffffd000  : vmalloc & ioremap
NR_IRQS:33
/axi@0/interrupt-controller@41200000: num_irq=2, edge=0x2
/axi@0/timer@41c00000: irq=1
clocksource: xilinx_clocksource: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604467 ns
xilinx_timer_shutdown
xilinx_timer_set_periodic
sched_clock: 32 bits at 100MHz, resolution 10ns, wraps every 21474836475ns
Calibrating delay loop... 49.35 BogoMIPS (lpj=246784)
pid_max: default: 4096 minimum: 301
Mount-cache hash table entries: 1024 (order: 0, 4096 bytes)
Mountpoint-cache hash table entries: 1024 (order: 0, 4096 bytes)
devtmpfs: initialized
cpu cpu0: Error -2 creating of_node link
clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns
NET: Registered protocol family 16
clocksource: Switched to clocksource xilinx_clocksource
NET: Registered protocol family 2
TCP established hash table entries: 1024 (order: 0, 4096 bytes)
TCP bind hash table entries: 1024 (order: 2, 20480 bytes)
TCP: Hash tables configured (established 1024 bind 1024)
UDP hash table entries: 128 (order: 0, 6144 bytes)
UDP-Lite hash table entries: 128 (order: 0, 6144 bytes)
NET: Registered protocol family 1
random: fast init done
workingset: timestamp_bits=30 max_order=14 bucket_order=0
io scheduler noop registered
io scheduler deadline registered
io scheduler cfq registered (default)
40600000.serial: ttyUL0 at MMIO 0x40600000 (irq = 2, base_baud = 0) is a uartlite
console [ttyUL0] enabled
console [ttyUL0] enabled
bootconsole [earlyser0] disabled
bootconsole [earlyser0] disabled
brd: module loaded
NET: Registered protocol family 17
Freeing unused kernel memory: 892K (c03ca000 - c04a9000)
This architecture does not have kernel memory protection.
Starting logging: OK
Initializing random number generator... done.
Starting network: OK

Welcome to Saturn V3 FPGA module - XC6SLX45 + Microblaze + Linux
saturn-v3 login:
Welcome to Saturn V3 FPGA module - XC6SLX45 + Microblaze + Linux
saturn-v3 login: root
# pwd
/root
# ls
# cd /cd
-sh: cd: can't cd to /cd
# cd /
# ls
bin      init     linuxrc  opt      run      tmp
dev      lib      media    proc     sbin     usr
etc      lib32    mnt      root     sys      var
#

