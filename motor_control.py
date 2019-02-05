import board
from digitalio import DigitalInOut, Direction, Pull
import busio

from pni_libs.debug import *
from pni_libs.rs485 import *

class motor_control:

    def __init__(self):
        self.serial_port = busio.UART(board.TX, board.RX, baudrate=9600, timeout=500)
        self.rts = DigitalInOut(board.D2)
        self.rts.direction = Direction.OUTPUT
        self.pull = Pull.DOWN
        self.transmit_timer = chronometer(time_length_ms = 1000)
        self.transmit_timer.start()
        print("motor init done")

    def update(self):
        if (self.transmit_timer.isDone()):
            self.transmit_timer.start()
            self.rts.value = True
            message = "Hello!\n"
            self.serial_port.write(bytearray(message))
            delay(100)
            self.rts.value = False
        else:
            return_message = self.serial_port.read()
            if return_message is not None:
                print(return_message)
