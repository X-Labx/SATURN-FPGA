- Setup a Ubuntu 14.01 Virtual Machine in VirtualBox and install the Xilinx Embedded version and also generate a license via the Xilinx website.
- Install the included board files to the */ISE_DS/EDK/board/ folder so the sub-directory would be NumatoLab/ipxact/Saturn_LX45_V3/data
- Now run xps in a new folder, setup the license in the license manager if needed.
- Either create a new project from scratch or open the included project.
- When you click export hardware to sdk, click export hardware only in the dialog.
- Now close xps and start xsdk from the command line.
- An example hardware project of the above steps is also included. 
- You may need to fix any issues with xsdk finding the compiler.
- Copy the elf file to a new directory
- Copy the system.bit and system_bd.bit from ~/micoblaze/SDK/SDK_Export/hw to the new directory too.
- Run: data2mem -bm system_bd.bmm -bd Test.elf -bt system.bit
- You will get a new bit file called system_rp.bit which can be programed into the board, you will need to use FT_Prog to setup the port B correctly first: Virtual COM port and RS232 UART (Do this in Windows 10, not Linux).
- Follow the instructions in the PDF to use the Flash config tool instead.
- Either use the VM to program the board if the usb JTAG programmer can be connected to it, or copy the bit file to a dedicated Linux machine and run impact.
- Now program the bit file using impact (you need to have setup the Xilinx tools previously correctly).
- In Linux run: sudo screen /dev/serial/by-id/usb-FTDI_Saturn_Spartan_6_FPGA_Module_FT6LDALU-if01-port0 9600
- The above command must be ran as sudo and the if01 corresponds to port B of the FT2232H.
- The following will be output:

--Starting Memory Test Application--
NOTE: This application runs with D-Cache disabled.As a result, cacheline requests will not be generated
Testing memory region: lpddr
    Memory Controller: axi_s6_ddrx
         Base Address: 0xa4000000
                 Size: 0x04000000 bytes 
          32-bit test: PASSED!
          16-bit test: PASSED!
           8-bit test: PASSED!
--Memory Test Application Complete--
