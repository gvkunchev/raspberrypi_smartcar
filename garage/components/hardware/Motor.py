#!/usr/bin/python
import RPi.GPIO as GPIO
from numpy import interp

class Motor(object):
  "Basic motor, that can turn forward and backward with adjustable speed"

  # Limitations for speed sent to PWM. The PWM constroller supports
  # 0-4095, but testing shows that these are the best useful limits.
  speedLimitOut = [
    500, # Minimum
    4000 # Maximum
  ]
  # Limitations for speed sent to Motor object. Using 0-100
  # so we can easily transform a percentage-like speed values.
  speedLimitIn = [
    0,  # Minimum
    100 # Maximum
  ]

  def __init__(self, pwm, pinFwd, pinBwd, pinSpeed):
    # param: pwm      - object  (The PWM controller that controls the speed of the motor)
    # param: pinFwd   - integer (The pin on Pi that controls the fwd motion)
    # param: pinBwd   - integer (The pin on Pi that controls the bwd motion)
    # param: pinSpeed - integer (The pin on the PWM controller that controls the speed)
    assert type(pinFwd)   is int, "The forward pin must be integer"
    assert type(pinBwd)   is int, "The backward pin must be integer"
    assert type(pinSpeed) is int, "The speed pin must be integer"
    self.pwm      = pwm
    self.pinFwd   = pinFwd
    self.pinBwd   = pinBwd
    self.pinSpeed = pinSpeed
    self._setGPIO()
    self._initSettgins()

  def _initSettgins(self):
    self.stop()
    self.setSpeed(50) # The middle of the valid range

  def _mapSpeed(self, speed):
    # param: speed - integer (The speed at which the motor should operate (0-100))
    # Maps speed in the speedLimitIn range to the corresponding value in the speedLimitOut range
    # Never returns a value out of the limits, no matter the input
    return int(interp(speed, self.speedLimitIn, self.speedLimitOut))

  def _setGPIO(self):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.pinFwd, GPIO.OUT)
    GPIO.setup(self.pinBwd, GPIO.OUT)

  def fwd(self):
    GPIO.output(self.pinFwd, GPIO.HIGH)
    GPIO.output(self.pinBwd, GPIO.LOW)

  def bwd(self):
    GPIO.output(self.pinBwd, GPIO.HIGH)
    GPIO.output(self.pinFwd, GPIO.LOW)

  def stop(self):
    GPIO.output(self.pinBwd, GPIO.LOW)
    GPIO.output(self.pinFwd, GPIO.LOW)

  def setSpeed(self, speed):
    # param: speed - integer (The speed at which the motor should operate (0-100))
    assert type(speed) is int, "The value for speed must be integer"
    speed = self._mapSpeed(speed)
    self.pwm.setValue(self.pinSpeed, 0, speed)

if __name__ == "__main__":
  pass