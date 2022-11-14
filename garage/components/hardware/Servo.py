#!/usr/bin/python
from numpy import interp

class Servo(object):
  "Servo that can rotate from about 0 o 180 degrees"

  # Limitations for turning sent to Servo object. Using 0-100
  # so we can easily transform a percentage-like turning values.
  limitIn = [
    0,  # Minimum
    100 # Maximum
  ]

  def __init__(self, pwm, port, minValue, maxValue):
    # param: pwm      - object  (The PWM controller that controls the speed of the motor)
    # param: port     - integer (The port on the PWM controller that controls the servo)
    # param: minValue - integer (The minimum value/angle that can be set for that servo)
    # param: maxValue - integer (The maximum value/angle that can be set for that servo)
    assert type(minValue) is int, "The value for minimum angle must be integer"
    assert type(maxValue) is int, "The value for maximum angle must be integer"
    self.pwm         = pwm
    self.port        = port
    self.limitOut    = [minValue, maxValue]
    self.value       = None
    self._initSettings()

  def _initSettings(self):
      self.home()

  def _mapValue(self, value):
    # param: value - integer (The value/angle that should be mapped (0-100))
    # Maps angle in the limitIn range to the corresponding value in the limitOut range
    # Never returns a value out of the limits, no matter the input
    return int(interp(value, self.limitIn, self.limitOut))

  def home(self):
    self.turn(50) # The middle of the valid range

  def turn(self, value):
    # param: value - integer (The value/angle that should be set (0-100))
    assert type(value) is int, "The value for rotational angle must be integer"
    value = self._mapValue(value)
    self.value = value
    self.pwm.setValue(self.port, 0, value)

  def getValue(self):
    return int(interp(self.value, self.limitOut, self.limitIn))

if __name__ == "__main__":
  pass