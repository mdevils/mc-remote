#!/usr/bin/python
import cwiid
import sys
import time
import threading

class WiimoteController:
	""" Wiimote controller """
	def __init__(self, mac):
		self.buttons = [ # Buttons key codes
			['1', 2],
			['2', 1],
			['-', 16],
			['+', 4096],
			['Home', 128],
			['A', 8],
			['B', 4],
			['Up', 2048],
			['Right', 512],
			['Down', 1024],
			['Left', 256]
		]
		self.mac = mac
		self.repeater = False
		self.on_key_down = False
		self.on_disconnect = False
		self.wiimote = False

	def connect(self):
		""" Opens wiimote connection """
		try:
			wiimote = self.wiimote = cwiid.Wiimote(self.mac)
			wiimote.mesg_callback = self.callback
			self.led = 0
			self.leds = [0, cwiid.LED1_ON, cwiid.LED2_ON, cwiid.LED3_ON, cwiid.LED4_ON]
			self.led_enable(1, True)
			wiimote.enable(cwiid.FLAG_MESG_IFC);
			wiimote.rpt_mode = 0 ^ cwiid.RPT_BTN
		except:
			return False
		return True

	def disconnect(self):
		""" Closes wiimote connection """
		if self.wiimote:
			try:
				self.wiimote.close()
				self.wiimote = False
			except:
				nothing = True # nothing
		if self.on_disconnect:
			self.on_disconnect()

	def notify(self, keys):
		if self.on_key_down:
			self.on_key_down(keys)
	
	def keydown(self, key_state): # I don't care about KeyUps
		""" Handles wiimote keydowns """
		keys = []
		for button in self.buttons:
			if (key_state & button[1]) == button[1]:
				keys += [button[0]]
		if self.repeater:
			self.repeater.stop()
			self.repeater = False
		if keys:
			self.notify(keys)
			self.repeater = WiimoteKeyRepeater(keys, self.notify)
			self.repeater.start()

	def callback(self, mesg_list, time):
		""" Handles wiimote messages """
		for mesg in mesg_list:
			if mesg[0] == cwiid.MESG_BTN: # button key/down
				self.keydown(mesg[1])
			elif mesg[0] ==  cwiid.MESG_ERROR: # disconnections
				self.disconnect()
			# I don't care about other messages

	def led_enable(self, num, enable):
		""" Enables or disables handlers """
		if enable:
			self.led = self.led | self.leds[num]
		else:
			self.led = (self.led | self.leds[num]) ^ self.leds[num]
		self.wiimote.led = self.led

class WiimoteKeyRepeater(threading.Thread):
	""" Repeats keydowns of Wiimote """
	def __init__ (self, keys, notifier):
		self.keys = keys
		self.notifier = notifier
		self.running = True
		threading.Thread.__init__(self, name="WiimoteKeyRepeater")

	def sleep(self, secs):
		""" Sleeps checking running param """
		value = 0
		while value < secs:
			if not self.running:
				return False
			value += 0.05
			time.sleep(0.05)
		return True

	def run(self):
		""" Repeats keydowns """
		if not self.sleep(0.5):
			return
		while self.running:
			self.notifier(self.keys)
			if not self.sleep(0.1):
				return

	def stop(self):
		""" Stops execution of repeater """
		self.running = False
		self.join()

