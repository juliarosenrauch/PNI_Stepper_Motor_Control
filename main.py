import board
import digitalio
import time
import motor_control

from pni_libs.debug import *
from pni_libs.helpers import *

class blinky_light_demo:

    def __init__(self, pin, duration):
        self.pin = pin
        self.duration = duration
        self.led = digitalio.DigitalInOut(self.pin)
        self.led.direction = digitalio.Direction.OUTPUT
        self.update_timer = chronometer(time_length_ms=duration)
        self.update_timer.start()
        self.reference_time = 0

    def led_on(self):
        self.led.value = True

    def led_off(self):
        self.led.value = False

    def update(self):

        if (self.update_timer.isDone()):
            self.update_timer.restart()
            if (self.led.value == True):
                self.led_off()
            else:
                self.led_on()


    # class function usage
    # def some_function():
    #    pass
    #   blink_light_demo.some_function()

if __name__ == "__main__":
    Debug.begin(debug_level = Debug.DEBUG)
    blinky_1 = blinky_light_demo(board.D13, 0.5)
    blinky_2 = blinky_light_demo(board.D12, 1)
    motor = motor_control.motor_control()

    while True:
        blinky_1.update()
        blinky_2.update()
        motor.update()
