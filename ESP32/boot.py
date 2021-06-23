# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl

import network
import os

# Connect to Wifi
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('WIFI', 'PASSWORD')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

# Start WebREPL
webrepl.start()
gc.collect()

# Check storage space
def df():
  s = os.statvfs('//')
  return ('{0} MB'.format((s[0]*s[3])/1048576))
