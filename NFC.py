#import RPi.GPIO as GPIO
from pn532 import *
from spi import *

class NFC:
	def __init__(self):
		pass;

	def setup(self):
		try:
			self.pn532 = PN532_SPI(debug=False, reset=20, cs=4)
			ic, ver, rev, support = self.pn532.get_firmware_version()
			print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

			# Configure PN532 to communicate with MiFare cards
			self.pn532.SAM_configuration()
		except:
			pass

	def listen(self):
		while True:
			try:
				# Check if a card is available to read
				uid = self.pn532.read_passive_target(timeout=0.5)
				# Try again if no card is available.
				if uid is None:
					continue
				uidStr = uid.hex()
				return uidStr
			except Exception as e:
				print(e)