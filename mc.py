#!/usr/bin/python
import sys
import time
from sendkeys import SendKeys
from wiimote import WiimoteController
sys.path.append('devices')
from acer_x1160 import AcerX1160

WIIMOTE_NO_ACTIVITY_TIMEOUT = 600 # Wiimote inactivity timeout. Saves battery energy.

class MediaCenter:
	""" Main class for controlling devices """
	def __init__(self):
		self.MODE_OFF	= 0
		self.MODE_XBMC	= 1
		self.MODE_TV	= 2
		self.mode = self.MODE_OFF
		self.sendkeys = SendKeys()
		self.sendkeys.send(self.sendkeys.ENTER)

		self.projector = AcerX1160()

		self.wiimote = WiimoteController()
		self.wiimote.on_key_down = self.key_down
		self.wiimote.on_disconnect = self.wiimote_reconnect

		self.wiimote_reconnect()

	def key_down(self, keys):
		""" Wiimote keydown handler """
		self.wiimote_no_activity_time = 0
		if len(keys) == 2:
			if keys[0] == '1':
				if keys[1] == 'A':
					self.mode = self.MODE_XBMC
					self.projector.power()
				if keys[1] == 'Home':
					self.mode = self.MODE_OFF
					self.projector.power()
				if keys[1] == 'B':
					self.projector.source()
		else:
			if len(keys) == 1:
				if keys[0] == 'Up':
					self.sendkeys.send(self.sendkeys.UP)
				if keys[0] == 'Down':
					self.sendkeys.send(self.sendkeys.DOWN)
				if keys[0] == 'Left':
					self.sendkeys.send(self.sendkeys.LEFT)
				if keys[0] == 'Right':
					self.sendkeys.send(self.sendkeys.RIGHT)
				if keys[0] == 'Home':
					self.sendkeys.send(self.sendkeys.TAB)
				if keys[0] == 'A':
					self.sendkeys.send(self.sendkeys.ENTER)
				if keys[0] == 'B':
					self.sendkeys.send(self.sendkeys.ESC)
				if keys[0] == '+':
					self.sendkeys.send(self.sendkeys.EQUALS)
				if keys[0] == '-':
					self.sendkeys.send(self.sendkeys.MINUS)
				

	def wiimote_reconnect(self):
		""" Reconnects to wiimote """
		self.wiimote_no_activity_time = 0
		while not self.wiimote.connect():
			connecting = True #nothing

media_center = MediaCenter()

while True:
	time.sleep(1)
	media_center.wiimote_no_activity_time += 1
	if media_center.wiimote_no_activity_time == WIIMOTE_NO_ACTIVITY_TIMEOUT:
		media_center.wiimote.disconnect()
	