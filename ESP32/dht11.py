from machine import Pin
from time import sleep
import dht

sensor = dht.DHT11(Pin(14))

avgtempC = 0
avgtempF = 0
avgHum = 0

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
            temp_f = temp * (9/5) + 32.0
            avgtempC += temp
            avgtempF += temp_f
            avgHum += hum
        except OSError as e:
            print('Failed to read sensor.')

    avgtempC /= 5
    avgtempF /= 5
    avgHum /= 5

    print('Avg Temperature: %3.1f C' %avgtempC)
    print('Avg Temperature: %3.1f F' %avgtempF)
    print('Avg Humidity: %3.1f %%' %avgHum)

if __name__ == "__main__":
    readDHT11()
