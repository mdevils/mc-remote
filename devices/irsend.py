#!/bin/python
import os

class IrSend:
	""" Class for sending IR-signals for devices, configured in /etc/lirc/lircd.conf """
	def send(self, device, command):
		""" Sends IR-signal to the device """
		os.system("irsend SEND_ONCE '" + device + "' '" + command + "'")
