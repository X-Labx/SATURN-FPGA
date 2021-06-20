from __future__ import print_function

import time
import random

#
# Need to install ftd2xx first
#
import ftd2xx

#
# Get info on ftd2xx devices, if any
#
serialnames = ftd2xx.listDevices()
if serialnames == None:
	serialnames = [" No Connected Devices "]

for i, s in enumerate(serialnames):
	if isinstance(s, unicode):
		serialnames[i] = unicodedata.normalize("NFC", s)

print("The Array is: ", serialnames)
# Output: The Array is:  ['FT6LDALUA', 'FT6LDALUB']

dev = ftd2xx.getDeviceInfoDetail(0)

print(dev)

#
# 0 is FT6LDALUA ; 1 is FT6LDALUB
# Needs to be set correctly for FPGA depending on which port A or B of FT2232H is being used 
#
dev = ftd2xx.openEx(ftd2xx.listDevices()[1])
dev.setTimeouts(5000, 5000)
dev.purge(ftd2xx.defines.PURGE_TX|ftd2xx.defines.PURGE_RX)
print("\nDevice Details :")
print("Serial : " , dev.getDeviceInfo()['serial'])
print("Type : " , dev.getDeviceInfo()['type'])
print("ID : " , dev.getDeviceInfo()['id'])
print("Description : " , dev.getDeviceInfo()['description'])

#
# 200Kb - if too small timing operations will cause a float exception
#
BLOCK_LEN = 2048 * 100

tx_data = str(bytearray([ random.randrange(0, 256) for i in range(BLOCK_LEN) ]))
print("\nWriting %d KB of data to the device..." % (BLOCK_LEN / 1024))
ts = time.time()
written = dev.write(tx_data)

rx_data = dev.read(BLOCK_LEN)
te = time.time()
print("\nReading %d KB of data from the device..." % (BLOCK_LEN / 1024))
p = te - ts

print("\nComparing data...\n")
if (tx_data == rx_data):
 print("Data written matches the data read\n")
else:
 print("Data verification failed\n") 

dev.close()
print("Transfer Time = %.3f seconds" % p)
speed = (BLOCK_LEN / 1024./1024 / p)

print("Transfer Rate = %.3f MB/s" % speed)

print("\nAsynchronous FIFO Test Finished")
