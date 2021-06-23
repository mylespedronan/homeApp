import time
from ustruct import unpack, unpack_from
from array import array

from machine import Pin, UART, I2C
import urequests as requests
import dht
import ujson as json
import espI2C as bme280
