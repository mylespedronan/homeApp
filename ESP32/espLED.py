# This file will be used to test turning an LED on using the GPIO pins

#### PINOUT ####
# Pin 0 = D3
# Pin 2 = D4 // Onboard LED
# Pin 4 = D2 // UART1
# Pin 5 = D1
# Pin 12 = D6
# Pin 13 = D7
# Pin 14 = D5
# Pin 15 = D8
################

from machine import Pin

pins = [Pin(i, Pin.OUT) for i in (0, 2, 5, 12, 13, 14, 15)]

def pinOn(i):
    pins[i].on()

def pinOff(i):
    pins[i].off()

if __name__ == "__main__":
    pinOn(i)
    pinOff(i)
