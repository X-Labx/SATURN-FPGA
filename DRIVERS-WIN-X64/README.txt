Instructions for setting up the FT2232H on Windows 10 for use with the board are below.

-Install Windows 10 and update. Updating is needed to get the device recognised usually.
-Plug in the board, next the device will be seen as "saturn xx" in device manager, but with an error as it needs a driver.
-Install the D2XX driver from https://ftdichip.com/drivers/d2xx-drivers/ there is usually an all in one exe as well as just the plain drivers in a zip file. Use the exe which is termed "WHQL Certified. Includes VCP and D2XX." (also included).
-Then unplug and plug in the board. From here FT_Prog and flash config tool should run correctly.

-Notes: It doesn't seem to work in Windows VM in Virutal Box for whatever reason, use a dedicated Windows 10 machine.

-Info: https://ftdichip.com/products/ft2232hq/

DISCLAIMER: There are no guarantees this will work for you. It is provided as is - and for reference, learning and for your own research purposes.