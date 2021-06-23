from iot import *
import time

def checkValue():
    data = get_json('### HTTP ###')

    #onboardLED(data['index']['ledRadio1'])
    tivaUart(data['index']['tivaLED'])
    dhtValues(data['dht']['name'])
    bmeValues(data['bme']['name'])

def onboardLED(x):
    if x == '0':
        pinOn(1)    # Onboard LED off
    else:
        pinOff(1)   # Onboard LED on

def tivaUart(x):
    if x == '1':
        uartRed()
    elif x == '2':
        uartGreen()
    elif x == '3':
        uartBlue()
    else:
        uart.write('a')

def dhtValues(x):
    if x  == 'fdsa':
        readDHT11()

def bmeValues(x):
    if x == 'fdsa':
        bme280_read()

while True:
    checkValue()
    time.sleep(5 - time.time() % 5)


# if __name__ == "__main__":
#     checkValue()
#     onboardLED()
