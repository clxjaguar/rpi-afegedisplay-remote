#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sudo apt-get install python-pip python-setuptools
# pip install --upgrade pip
# sudo pip install -U pyserial
#
# do not forget "dtoverlay=pi3-disable-bt" even on RPI2!

import os, sys, serial, time, io, glob, re, datetime

WIDTH = 20
LINES = 8

serialport = serial.Serial('/dev/ttyAMA0', 1200, xonxoff=False, rtscts=False, dsrdtr=False, timeout=0, parity=serial.PARITY_ODD)
daysofweek={0:u'Lundi', 1:u'Mardi', 2:u'Mercredi', 3:u'Jeudi', 4:u'Vendredi', 5:u'Samedi', 6:u'Dimanche'}
months={1:u'janvier', 2:u'février', 3:u'mars', 4:u'avril', 5:u'mai', 6:u'juin', 7:u'juillet', 8:u'août', 9:u'septembre', 10:u'octobre', 11:u'novembre', 12:u'décembre'}

aff_state = {}

def DisplaySetCoordX(x):
	global aff_state
	aff_state['x']=x
	if aff_state['x'] < 0:
		aff_state['x'] = 0
	if aff_state['y'] == aff_state['height'] -1:
		return
	if aff_state['x'] >= aff_state['width']:
		aff_state['x'] = aff_state['width'] - 1

def DisplaySetCoordY(y):
	global aff_state
	aff_state['y']=y
	if aff_state['y'] < 0:
		aff_state['y'] = 0
	if aff_state['y'] >= aff_state['height']:
		aff_state['y'] = aff_state['height'] - 1

def DisplaySetCoordsXY(x, y):
	DisplaySetCoordX(x)
	DisplaySetCoordY(y)

def DisplaySetCoordRelX(dx):
	global aff_state
	DisplaySetCoordX(aff_state['x'] + dx)

def DisplaySetCoordRelY(dy):
	global aff_state
	DisplaySetCoordY(aff_state['y'] + dy)

def DisplaySend(bytes):
	global serialport, aff_state
	for byte in bytes:
		if aff_state['debug']:
			print("%02X" % ord(chr(byte)),)
			sys.stdout.flush()
		s = bytearray()
		s.append(byte)
		serialport.write(s)
		time.sleep(0.06) #0.05 is not enough
	aff_state['last_send'] = time.time()


dict = {u'1':[0x02,0x82], u'2':[0x03,0x83], u'3':[0x04,0x84], u'4':[0x05,0x85], u'5':[0x06,0x86], u'6':[0x07,0x87], u'7':[0x08,0x88], u'8':[0x09,0x89], u'9':[0x0A,0x8A], u'0':[0x0B,0x8B],
        u'!':[0x2a,0x02,0xAA,0x82], u'@':[0x2a,0x03,0xAA,0x83], u'#':[0x2a,0x04,0xAA,0x84], u'$':[0x2a,0x05,0xAA,0x85], u'%':[0x2a,0x06,0xAA,0x86], u'^':[0x2a,0x07,0xAA,0x87], u'&':[0x2a,0x08,0xAA,0x88], u'*':[0x2a,0x09,0xAA,0x89], u'(':[0x2a,0x0A,0xAA,0x8A], u')':[0x2a,0x0B,0xAA,0x8B],
        u',':[0x33,0xB3], u'.':[0x34,0xB4], u'/':[0x35,0xB5], u' ':[0x39,0xB9],
        u'a':[0x1E,0x9E], u'b':[0x30,0xB0], u'c':[0x2E,0xAE], u'd':[0x20,0xA0], u'e':[0x12,0x92], u'f':[0x21,0xA1], u'g':[0x22,0xA2], u'h':[0x23,0xA3], u'i':[0x17,0x97], u'j':[0x24,0xA4], u'k':[0x25,0xA5], u'l':[0x26,0xA6], u'm':[0x32,0xB2], u'n':[0x31,0xB1], u'o':[0x18,0x98], u'p':[0x19,0x99], u'q':[0x10,0x90], u'r':[0x13,0x93], u's':[0x1F,0x9F], u't':[0x14,0x94], u'u':[0x16,0x96], u'v':[0x2F,0xAF], u'w':[0x11,0x91], u'x':[0x2D,0xAD], u'y':[0x15,0x95], u'z':[0x2C,0xAC],
        u'A':[0x2A,0x1E,0xAA,0x9E], u'B':[0x2A,0x30,0xAA,0xB0], u'C':[0x2A,0x2E,0xAA,0xAE], u'D':[0x2A,0x20,0xAA,0xA0], u'E':[0x2A,0x12,0xAA,0x92], u'F':[0x2A,0x21,0xAA,0xA1], u'G':[0x2A,0x22,0xAA,0xA2], u'H':[0x2A,0x23,0xAA,0xA3], u'I':[0x2A,0x17,0xAA,0x97], u'J':[0x2A,0x24,0xAA,0xA4], u'K':[0x2A,0x25,0xAA,0xA5], u'L':[0x2A,0x26,0xAA,0xA6], u'M':[0x2A,0x32,0xAA,0xB2], u'N':[0x2A,0x31,0xAA,0xB1], u'O':[0x2A,0x18,0xAA,0x98], u'P':[0x2A,0x19,0xAA,0x99], u'Q':[0x2A,0x10,0xAA,0x90], u'R':[0x2A,0x13,0xAA,0x93], u'S':[0x2A,0x1F,0xAA,0x9F], u'T':[0x2A,0x14,0xAA,0x94], u'U':[0x2A,0x16,0xAA,0x96], u'V':[0x2A,0x2F,0xAA,0xAF], u'W':[0x2A,0x11,0xAA,0x91], u'X':[0x2A,0x2D,0xAA,0xAD], u'Y':[0x2A,0x15,0xAA,0x95], u'Z':[0x2A,0x2C,0xAA,0xAC],
        u'é':[0x5b,0xdb], u'[':[0x1a,0x9a], u']':[0x1b,0x9b], u'£':[0x6D,0xED], u'ä':[0x5C,0xDC], u'å':[0x5D,0xDD], u'ç':[0x5A,0xDA], u'ò':[0x64,0xE4], u'ü':[0x65,0xE5], u'ñ':[0x5F,0xDF],
        u'É':[0x2A,0x5B,0xAA,0xDB], u'ú':[0x2A,0x66,0xAA,0xE6], u'ë':[0x2a,0x68,0xaa,0xe8], u'í':[0x2A,0x63,0xAA,0xE3], u'ï':[0x2A,0x69,0xAA,0xE9], u'Ö':[0x2A,0x5E,0xAA,0xDE], u'Ä':[0x2A,0x5C,0xAA,0xDC], u'Æ':[0x2A,0x6E,0xAA,0xEE], u'ë':[0x2A,0x68,0xAA,0xE8], u'á':[0x2A,0x61,0xAA,0xE1], u'Å':[0x2A,0x5D,0xAA,0xDD], u'Ç':[0x2A,0x5A,0xAA,0xDA], u'ó':[0x2A,0x64,0xAA,0xE4], u'Ü':[0x2A,0x65,0xAA,0xE5], u'Ñ':[0x2A,0x5F,0xAA,0xDF],
        u'ß':[0x60,0xE0], u'æ':[0x6E,0xEE], u'ê':[0x68,0xE8], u'â':[0x67,0xE7], u'à':[0x61,0xE1], u'-':[0x0C,0x8C], u'=':[0x0D,0x8D], u'\'':[0x28,0xA8],u'’':[0x28,0xA8], u'‘':[0x29,0xa9],
        u'\\':[0x2B,0xAB],u'ô':[0x6a,0xea], u'ö':[0x5e,0xde], u'î':[0x69,0xe9], u'ì':[0x63,0xe3], u'ÿ':[0x6c,0xec], u'û':[0x6b,0xeb], u'ù':[0x66,0xe6], u'è':[0x62,0xe2],
        u'+':[0x2A,0x0D,0xAA,0x8D], u'"':[0x2A,0x28,0xAA,0xA8], u'|':[0x2A,0x2B,0xAA,0xAB], u'~':[0x2A,0x29,0xAA,0xA9], u'_':[0x2A,0x0C,0xAA,0x8C], u':':[0x2A,0x27,0xAA,0xA7], u'{':[0x2A,0x1A,0xAA,0x9A], u'}':[0x2A,0x1B,0xAA,0x9B],
        u'?':[0x2A,0x35,0xAA,0xB5], u'<':[0x2a,0x33,0xaa,0xba], u'>':[0x2a,0x34,0xaa,0xb4], u';':[0x27,0xa7]}

def DisplaySendChar(char):
	global dict,aff_state
	x = aff_state['x']
	y = aff_state['y']
	aff_state['output'][y] = aff_state['output'][y][:x] + char + aff_state['output'][y][x+1:]
	try:
		codes = dict[char]
	except KeyError:
		codes = dict[' ']
	DisplaySetCoordRelX(1)
	DisplaySend(codes)
	time.sleep(0.1)

def DisplaySendString(string):
	for char in string:
		DisplaySendChar(char)

def DisplaySendEnterKey():
	global aff_state
	DisplaySend([0x1c,0x9c])
	if (aff_state['y'] == aff_state['height']-1):
		DisplaySetCoordY(0)
	else:
		DisplaySetCoordRelY(1)
	DisplaySetCoordX(0)
	time.sleep(0.1)

def DisplaySendTabKey():
	DisplaySend([0x0f,0x8f])
	time.sleep(0.1)

def DisplaySendEscKey():
	DisplaySend([0x01])
	time.sleep(0.1)

def DisplaySendLeftKey():
	DisplaySetCoordRelX(-1)
	DisplaySend([0x4b,0xcb])

def DisplaySendRightKey():
	DisplaySetCoordRelX(1)
	DisplaySend([0x4d,0xcd])

def DisplaySendUpKey():
	DisplaySetCoordRelY(-1)
	DisplaySend([0x48,0xc8])
	time.sleep(0.1)

def DisplaySendDownKey():
	DisplaySetCoordRelY(1)
	DisplaySend([0x50,0xd0])
	time.sleep(0.1)

def DisplaySendHomeKey():
	DisplaySetCoordX(0)
	DisplaySend([0x47,0xc7])
	time.sleep(0.1)

def DisplaySendEndKey():
	global aff_state
	aff_state['x'] = aff_state['width'] - 1
	DisplaySend([0x4f,0xcf])
	time.sleep(0.1)

def DisplaySendPgUpKey():
	DisplaySetCoordX(0)
	DisplaySetCoordY(0)
	DisplaySend([0x49,0xc9])
	time.sleep(0.1)

def DisplaySendPgDownKey():
	DisplaySetCoordX(0)
	DisplaySetCoordY(0)
	DisplaySend([0x51,0xd1])
	time.sleep(0.1)

def DisplaySendFunctionKey(fkey):
	if fkey == 1:
		DisplaySend([0x3B,0xBB])
	if fkey == 2:
		DisplaySend([0x3C,0xBC])
	if fkey == 3:
		DisplaySend([0x3D,0xBD])
	if fkey == 4:
		DisplaySend([0x3E,0xBE])
	if fkey == 5:
		DisplaySend([0x3F,0xBF])
	if fkey == 6:
		DisplaySend([0x40,0xC0])
	if fkey == 7:
		DisplaySend([0x41,0xC1])
	if fkey == 8:
		DisplaySend([0x42,0xC2])
	if fkey == 9:
		DisplaySend([0x43,0xC3])
	if fkey == 10:
		DisplaySend([0x44,0xC4])
	time.sleep(0.3)

def DisplayCaplockToggle():
	DisplaySend([0x3a, 0xba])
	time.sleep(0.3)

def DisplayInsmodeToggle():
	DisplaySend([0x52, 0xd2])
	time.sleep(0.1)

def DisplaySendDel():
	DisplaySend([0x53, 0xd3])

def DisplaySendBackspace():
	DisplaySetCoordRelX(-1)
	DisplaySend([0x0E, 0x8E])

def DisplayIdle():
	DisplaySend([0xaa, 0x9d, 0xb8, 0x81])

def DisplayClearScreen():
	DisplaySetCoordsXY(0, 0)
	DisplaySendFunctionKey(10)
	#DisplaySendString('o') # needed sometimes?
	#DisplaySendBackspace()
	DisplayResetOutputBuffer()
	DisplaySetCoordsXY(0, 0)

def DisplayResetOutputBuffer():
	global aff_state
	DisplaySetCoordsXY(0, 0)
	for i in range(aff_state['height']):
		aff_state['output'][i] = ' '.ljust(aff_state['width'])
		aff_state['diffline'][i] = 0

def DisplayInit():
	global aff_state
	aff_state['x'] = 0
	aff_state['y'] = 0
	aff_state['width'] = WIDTH
	aff_state['height'] = LINES
	aff_state['debug'] = False
	aff_state['input'] = {}
	aff_state['output'] = {}
	aff_state['diffline'] = {}
	aff_state['diffscreen'] = 0
	DisplayResetOutputBuffer()
	for i in range(15):
		DisplaySendEscKey()
	DisplayIdle()
	time.sleep(0.50)
	DisplaySendTabKey()
	time.sleep(0.50)
	DisplaySendEnterKey()
	DisplayIdle()
	DisplaySendChar('1')
	DisplayIdle()
	time.sleep(0.50)
	DisplaySendEnterKey()
	DisplayResetOutputBuffer()
	DisplayIdle()

def DisplayPark():
	global aff_state
	if (aff_state['y'] == aff_state['height']-1) and (aff_state['x'] == aff_state['width']):
		DisplayIdle()
		return

	DisplaySendEndKey()
	while (aff_state['y'] < aff_state['height']-1):
		DisplaySendDownKey()
	DisplaySendRightKey()

def DisplayReadFile(filename):
	global aff_name, daysofweek, months
	now = datetime.datetime.today()
	dayofweek = daysofweek[now.weekday()]
	dayofmonth = str(now.day)
	month = months[now.month]
	hour = "%02d:%02d"%(now.hour, now.minute)

	i=0
	if filename != '':
		try:
			f = io.open(filename, 'r', encoding="utf-8")
			try:
				for line in f:
					text = line.replace("\n", "")
					text = text.replace("{HEURE}", hour)
					text = text.replace("{JOUR}", dayofweek)
					text = text.replace("{NJOUR}", dayofmonth)
					text = text.replace("{MOIS}", month)
					aff_state['input'][i] = text[:aff_state['width']].center(aff_state['width'])
					i+=1
			except UnicodeDecodeError:
				aff_state['input'][i] = u'UnicodeDecodeError'.center(20)
				i+=1
			f.close()
		except:
			aff_state['input'][i] = u'File Error!'.center(20)
	while (i<aff_state['height']):
		aff_state['input'][i] = u' '.ljust(aff_state['width'])
		i+=1

def DisplayNeedUpdateCheck():
	global aff_state
	aff_state['diffscreen'] = 0
	for y in range(aff_state['height']):
		if aff_state['input'][y] != aff_state['output'][y]:
			aff_state['diffline'][y] = 1
			aff_state['diffscreen'] = 1
		else:
			aff_state['diffline'][y] = 0
	return aff_state['diffscreen']

def MakeFileChoice(path):
	filelist = glob.glob(path+'/[0-9]*.txt')
	files = {}
	for file in filelist:
		try:
			if os.path.getsize(file) > 3:
				priority = int(re.search('[0-9]+', file[file.rfind('/'):]).group(0))
				files[file] = {}
				files[file]['age'] = time.time() - os.path.getmtime(file)
				files[file]['priority'] = priority
		except:
			print ('error:', sys.exc_info()[1])

	files = sorted(files.iteritems(), key=lambda key: (key[1]['priority'], key[1]['age']))
	for filename, file in files:
		if ((file['priority'] < 10 and file['age'] > 3600)
		or (file['priority'] < 30 and file['age'] > 86400)):
			continue
		return filename
	return ''

def main(argv):
	global aff_state

	oldfile = ''
	if len(argv) < 2:
		sys.stderr.write("This program control a AFEGE public LED display and uses a directory containing .txt files as data source. \n")
		sys.stderr.write("Filenames need to have a number in it for priority management and files are ignored if empty. \n\n")
		sys.stderr.write("Usage: %s <directory>\n\n" % argv[0])
		sys.exit(-1)

	while True:
		DisplayInit()
		while True:
			file = MakeFileChoice(argv[1])
			DisplayReadFile(file)

			if (time.time() - aff_state['last_send'] > 8):
				break

			if not DisplayNeedUpdateCheck():
				DisplayPark()
				time.sleep(2)
				continue

			if file != oldfile:
				print ('['+file+']')
				DisplayClearScreen()
				DisplayNeedUpdateCheck()
				oldfile = file

			if aff_state['x'] >= aff_state['width']:
				DisplaySendEnterKey()

			if aff_state['diffline'][aff_state['y']]:
				sys.stdout.write(str(aff_state['y'])+'\t')
				for x in range(aff_state['width']):
					if aff_state['input'][aff_state['y']][aff_state['x']:] == aff_state['output'][aff_state['y']][aff_state['x']:]:
						break
					try:
						sys.stdout.write(aff_state['input'][aff_state['y']][aff_state['x']]);
					except:
						sys.stdout.write('?')
					sys.stdout.flush()
					DisplaySendChar(aff_state['input'][aff_state['y']][aff_state['x']])
				sys.stdout.write('\n')

			if DisplayNeedUpdateCheck():
				DisplaySendEnterKey()
				#DisplaySendHomeKey()


if __name__ == "__main__":
    main(sys.argv)
