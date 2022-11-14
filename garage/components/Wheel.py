#!/usr/bin/python
from hardware.Servo import Servo

class Wheel(object):
  "Wheel that can make the care turn left/right"

  def __init__(self, pwm, port, min, max):
    # param: pwm  - object  (The PWM controller that controls the speed of the motor)
    # param: port - integer (The port on the PWM controller that controls the steering servo)
    # param: min  - integer (The minimum value/angle at which the steering servo can rotate)
    # param: max  - integer (The maximum value/angle at which the steering servo can rotate)
    self.servo = Servo(pwm, port, min, max)

  def turnLeft(self):
    self.servo.turn(0) # The minimum from the valid range

  def turnRight(self):
    self.servo.turn(100) # The maximum from the valid range

  def home(self):
    self.servo.turn(50) # The middle of the valid range

  def turn(self, value):
    # param: value - integer (The value/angle that should be set (0-100))
    self.servo.turn(value)

if __name__ == "__main__":
  pass
