from machine import UART

uart = UART(1, baudrate=115200)

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

if __name__ == "__main__":
    uartRed()
    uartGreen()
    uartBlue()
    uartS1()
    uartS2()
