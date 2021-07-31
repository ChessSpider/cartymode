# Installation

## Hardware required

- Raspberry Pi 2 Model B or better
- Pican2, or any CAN-hardware device

## Software

You need to install the following software on the Raspberry Pi:

```
 $ apt install wireshark can-utils
```

After, optionally but recommended, make the canstuff start on boot.

Update _/etc/modules_:

> can  
> can_raw  
> can_dev  
> vcan

## Add virtual can adapter

Add a virtual can adapter if you want to test on a virtual can network. Please note; you must repeat this after a reboot

```
#!/bin/bash
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

Tip: Set this in a file /usr/vcanstart

## Activate can0 adapter

Use this if the RPI is attached to the car. Please note; you must repeat this after a reboot

```
#!/bin/bash
 sudo ip link set can0 type can bitrate 500000
 sudo ifconfig can0 up
```

Tip: Set this in a file /usr/canstart

## Next

Run wireshark on it (either virtual or real canbus), replay canbus logfile on the vcan, ???, profit!

# Useful commands

Dump can0 into a logfile, with delta-timestamps. Output to logfile and stdout.  
`candump -t d -L -l -s 0 can0`

Replay a logfile for an infinite number of times onto can0  
`canplayer -I <infile -l i -v`

Sniff a canbus and highlight changing bytes with colour  
`cansniffer -c can0`

Send a message with priority id 123 onto the canbus  
`cansend can0 123#DEADBEEF`

Only record certain canbus msg
`candump -t d -L -l -s 0 can0,652:FFFFFFFF,252:FFFFFFFF,552:FFFFFFFF`
