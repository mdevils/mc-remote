#!/bin/python
import irsend
import time

class DefenderHollywood95(irsend.IrSend):
	""" Ir-send implementation for Defender Hollywood 95 projector """
	def __init__(self):
		self.turned_on = False
	
	def command(self, cmd):
		""" Sends command to the speakers """
		self.send("Defender_Hollywood_95", cmd)

	def vol_up(self):
		self.command('VolumeUp')

	def vol_down(self):
		self.command('VolumeDown')

	def power(self):
		self.command('Power')	