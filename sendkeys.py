#!/bin/python
import os

class SendKeys:
	""" Sends key codes to X-Window system """
	def __init__(self):
		""" Inits Linux-specific key codes """
		self.ESC = 9
		self.LEFT = 113
		self.UP = 111
		self.DOWN = 116
		self.RIGHT = 114
		self.ENTER = 36
		self.TAB = 23
		self.EQUALS = 21
		self.MINUS = 20
		
	def send(self, code):
		""" Sends IR-signal to the device """
		os.system("xsendkeycode '" + str(code) + "' 0")
