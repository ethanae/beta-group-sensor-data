from gpiozero import DigitalInputDevice
import time


def get_reading():
	d0_input = DigitalInputDevice(21)
	if not d0_input.value:
		print("moisture threshold reached")
		return 0
	else:
		print("needs water")
		return 1
