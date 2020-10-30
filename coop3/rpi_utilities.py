import RPi.GPIO as gpio
from time import monotonic_ns

"""
Call the update function to find out if the pin has changed

To import the library
from rpi_utilities import debounce

In your __init__ function
self.somePinName = debounce(pin=UP_PROX, delay=0.001)
self.somePinState = 0

In your fast running thread
self.somePinState = self.somePinName.update()
if self.somePinState != None:
	print(f'Some Pine Value is {self.somePinState}')
"""

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

OPEN = 0
CLOSED = 1
WAITING = 2

class debounce():
	def __init__(self, *args, **kwargs):
		if 'pin' in kwargs:
			self.pin = kwargs.get('pin')
			gpio.setup(self.pin, gpio.IN,pull_up_down=gpio.PUD_DOWN)
			#print(f'Pin is {self.pin}')
			if gpio.input(self.pin) == 0:
				self.state = OPEN
			if gpio.input(self.pin) == 1:
				self.state = CLOSED
			self.start = 0
		if 'delay' in kwargs:
			self.ns_delay = int(kwargs.get('delay') * 1000000000)
		else:
			self.ns_delay = int(0.1 * 1000000000)

	def update(self):
		pin_state = gpio.input(self.pin)
		if self.state != pin_state and self.state != WAITING:
			self.start = monotonic_ns()
			self.state = WAITING
			#print(f'Start {self.start}')
		if self.state == WAITING:
			now = monotonic_ns()
			duration = now - self.start
			#print(f'Duration {duration}')
			if duration > self.ns_delay:
				self.state = pin_state
				print(f'Pin {self.pin} New State is {self.state}')
				return self.state

	def current(self):
		return gpio.input(self.pin)
