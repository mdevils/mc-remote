#!/bin/python
import irsend
import time

class AcerX1160(irsend.IrSend):
	""" Ir-send implementation for Acer X1160 projector """
	def __init__(self):
		self.turned_on = False
	
	def command(self, cmd):
		""" Sends command to the projector """
		self.send("Acer_X1160", cmd)

	def power(self):
		""" Turns on/off the projector """
		self.command('Power')
		time.sleep(0.5)
		self.command('Power')

	def source(self):
		""" Changes source of the projector """
		self.command('Source')
