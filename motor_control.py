import board
from digitalio import DigitalInOut, Direction, Pull
import busio

from pni_libs.debug import *
from pni_libs.rs485 import *

class motor_control:

    def __init__(self):
        Debug.msg("Configuring...", Debug.INFO, source='motor')
        self._baudrate = 9600
        self.serial_port = busio.UART(board.TX, board.RX, baudrate=9600, timeout=500)
        self.rts = DigitalInOut(board.D2)
        self.rts.direction = Direction.OUTPUT
        self.pull = Pull.DOWN
        self.transmit_timer = chronometer(time_length_ms = 1000)
        self.transmit_timer.start()
        Debug.msg("Motor controller initialization done", Debug.INFO, source="motor")

    def motor_send(self, msg):
        self.rts.value = True
        out_msg = ''.join(["/", msg, "\r"])
        print(out_msg)
        #Debug.msg("sending {}".format(out_msg), Debug.INFO, source="motor")
        self.serial_port.write(bytearray(out_msg))
        delay(self.delay_length(len(out_msg)))
        self.rts.value = False

    def delay_length(self, msg_length):
        # correction factor of 1.2 is applied
        return (msg_length*8.0)/self._baudrate*1000*1.2

    def motor_receive(self):
        return_messages = self.serial_port.read()

        if (return_message is not None):
            response_str = ''.join([chr(b) for b in return_message])
            response_str.replace("\r","")
        else:
            response_str = None
            return response_str

    def update(self):
        if (self.transmit_timer.isDone()):
            self.transmit_timer.start()
            self.motor_send("1QR")
                # 1m20V10000P0R
            # 1 is the address
            # m is power
            # 20 is the percentage of the power
            # V is velocity in microsteps/second,
            # P designates positive direction to turn
            # the number after it is how far to go
            # R is execute
            # \r is end of line character

        else:
            return_message = self.serial_port.read()
            if return_message is not None:
                Debug.msg(return_message, Debug.INFO, source="motor")

    def parse_motor_response(self, response):
        # example response
        # [weird]/0[status]
        response = bytearray(response)
        status_byte = response[3]

        busy = status_byte & 0x20
        error = status_byte & 0b1111
        
        pass
