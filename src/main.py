#!/usr/bin/python
import soil
import bmp180


def get_readings():
	print(bmp180.get_readings())
	print(soil.get_reading())
get_readings()
