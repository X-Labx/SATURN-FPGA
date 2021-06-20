Read the notes and points below to setup and run.

Hardware:
-Use the included ISE project to generate a bit and bin file (the project is for 14.7 ISE (last version)), created in an Ubuntu Virtual Machine 20.04 originally.
-The top.v file is a wrapper module to provide a auto reset since the board doesn't have any buttons 
-You need to set binary in bitgen to generate bin file too, which is used by the config tool to program the flash.
-The bit file can be used with an appropriate JTAG programmer.

Programming (Windows 10):
-Transfer the bin or bit file to a Windows 10 machine.
-Windows drivers for FT2232H chip as well as FT Prog need to have been setup correctly beforehand (your responsibility).
-You need to configure the board FT2232H chip to be in the correct mode using FT_Prog as follows:
--Port B: 245 FIFO ; D2XX Direct driver
-Program the board with the bin (Flash tool) or bit file (via JTAG).

Software:
-To communicate with the board setup Python on Windows 10 and ensure it is in the Windows path, and install the ftd2xx Python package.
--A Python 2.7.18 msi installer is included and was used for verification.
-- Install the ftd2xx package with: pip install ftd2xx.
-Now connect the board, check the setup with FT_Prog if needed (see above), and run the test script in a Windows command prompt with: python script.py
-You need to make sure the Python script is also using correct port i.e., [1] not [0] in script.

DISCLAIMER: There are no guarantees this will work for you. It is provided as is - and for reference, learning and for your own research purposes.

