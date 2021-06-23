from machine import Pin, UART, I2C
from time import sleep
import urequests as requests
import dht
import ujson as json
import espI2C as bme280

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
pins = [Pin(i, Pin.OUT) for i in (0, 2, 5, 12, 13, 14, 15)]
uart = UART(1, baudrate=115200)

sensor = dht.DHT11(Pin(14))

avgtempC = 0
avgtempF = 0
avgHum = 0

def uartRed():
    uart.write('r')

def uartGreen():
    uart.write('g')

def uartBlue():
    uart.write('b')

def uartS1():
    uart.write('1')

def uartS2():
    uart.write('2')

def pinOn(i):
    pins[i].on()

def pinOff(i):
    pins[i].off()

def get_json(url):
    return requests.get(url).json()

def readDHT11():
    global avgtempC
    global avgtempF
    global avgHum

    for i in range(0, 5):
        try:
            sleep(1)
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            temp_f = (temp * (9/5)) + 32.0
            avgtempC += temp
            avgtempF += temp_f
            avgHum += hum
        except OSError as e:
            print('Failed to read sensor.')

    avgtempC /= 6
    avgtempF /= 6
    avgHum /= 6

    payload = {
        'tempc' : avgtempC,
        'tempf' : avgtempF,
        'hum' : avgHum
    }

    headers = {'Content-Type':'application/json'}
    r = requests.post("### HTTP ### /dht/data", json=payload, headers=headers)

    if r.status_code == 200:
        print("\nMessage Received : " + r.text)
    else:
        print("Bad Message \n" + r.text)

    print('Avg Temperature: %3.1f C' %avgtempC)
    print('Avg Temperature: %3.1f F' %avgtempF)
    print('Avg Humidity: %3.1f %%' %avgHum)

    r.close()

def bme280_read():
    bme = bme280.BME280(i2c=i2c)
    tempc, pres, hum = bme.read_compensated_data()
    tempf = (tempc * (9/5)) + 32.0
    sealevel = bme.sealevel
    altitude = bme.altitude
    dewpoint = bme.dew_point

    payload = {
        'tempc' : tempc,
        'tempf' : tempf,
        'pres' : pres,
        'hum' : hum,
        'sealevel' : sealevel,
        'altitude' : altitude,
        'dewpoint' : dewpoint
    }

    headers = {'Content-Type':'application/json'}
    r = requests.post("### HTTP ### /bme/data", json=payload, headers=headers)

    if r.status_code == 200:
        print("\nMessage Received : " + r.text)
    else:
        print("Bad Message \n" + r.text)

    print('BME Temp C: %3.1f C' % tempc)
    print('BME Temp F: %3.1f F' % tempf)
    print('BME Pressure: %3.1f hPa' % pres)
    print('BME Humidity: %3.1f %%' % hum)
    print('BME Sea Level: %3.1f PA' % sealevel)
    print('BME Altitude: %3.1f m' % altitude)
    print('BME Dew Point: %3.1f C' % dewpoint)

    r.close()

if __name__ == "__main__":
    pinOn(i)
    pinOff(i)
    uartRed()
    uartGreen()
    uartBlue()
    uartS1()
    uartS2()
    get_json(url)
    readDHT11()
