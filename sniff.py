#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sudo apt-get install python-pip python-setuptools
# pip install --upgrade pip
# sudo pip install -U pyserial
#
# do not forget "dtoverlay=pi3-disable-bt" even on RPI2 for parity!

import os, sys, serial, time
serialport = serial.Serial('/dev/ttyAMA0', 1200, xonxoff=False, rtscts=False, dsrdtr=False, timeout=0, parity=serial.PARITY_ODD)

def send(*bytes):
	global serialport
	for byte in bytes:
		print "->%02X" % ord(chr(byte)),
		serialport.write(chr(byte))
		sys.stdout.flush()
		time.sleep(0.10)

for i in range(20):
	send(0x01)
	time.sleep(0.05)

send(0xaa, 0x9d, 0xb8, 0x81)
send(0x0F)
time.sleep(0.20)
send(0xaa, 0x9d, 0xb8, 0x81)
send(0x1c, 0x9c)
send(0xaa, 0x9d, 0xb8, 0x81)
send(0x03, 0x83)
send(0xaa, 0x9d, 0xb8, 0x81)
send(0x1c, 0x9c)

lasttime = time.time()
lastptime = 0
count = 0
while True:
	c = serialport.read(1)
	duration = time.time()-lasttime
	if len(c) == 0:
		if duration>10:
			send(0xaa, 0x9d, 0xb8, 0x81)
			lasttime = time.time()
		continue

	serialport.write(c)

	lasttime = time.time()
	count+=1
	if duration > 0.15:
		count=0

	if (ord(c) == 0xAA and count==0): continue
	if (ord(c) == 0x9D and count==1): continue
	if (ord(c) == 0xB8 and count==2): continue
	if (ord(c) == 0x81 and count==3): continue


	if (time.time()-lastptime) > 0.5:
		sys.stdout.write("\n\a")
	lastptime = time.time()

	#if duration > 0.11:
	#	print " [%.2f]" % duration,
	sys.stdout.write("0x%02X," % ord(c))
	sys.stdout.flush()
