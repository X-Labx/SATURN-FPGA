Instructions are below on how to setup an Ethernet project on the Saturn board. You will need a saturn board, breakout board and an ethernet board (connect to header 2) connected to your Windows 10 machine.

Either build an EDK project, export the hardware and then create an echo server app in xsdk from scractch. Or use the example in the zip file.
Program the bit file, open a serial port termial at 9800 baud and then run the app (Run As -> Launch on Hardware). The following will be output (or similiar).

MAC ID : 0x80 0x1F 0x12 0x65 0x22 0x8A


-----lwIP TCP echo server ------

---TCP packets sent will be echoed back---

Board IP: 192.168.0.99

Netmask : 255.255.255.0

Gateway : 192.168.0.1

auto-negotiated link speed: 100
TCP echo server started @ port 23

Now setup your Windows connection via Ethernet Properties -> Internet Protocol V4 Properties - in the box add an IP incremented by one (e.g., 192.168.0.100) corresponding to the output IP (above). Now add the same Netmask and Gateway details and close the window.

Open a Putty telnet connection using the board's IP and open port, next type characters which should be relayed back if everything is working.

Try using Wireshark to also see the traffic back and forth.