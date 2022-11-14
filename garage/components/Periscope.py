#!/usr/bin/python
from hardware.Servo import Servo

class Periscope(object):
  "This is a representation of the camera holder and its two servos"

  def __init__(self, pwm, portX, portY, minX, maxX, minY, maxY, span):
    # param: pwm   - object  (The PWM controller that controls the speed of the motor)
    # param: portX - integer (The port for the x-servo on the PWM controller)
    # param: portY - integer (The port for the y-servo on the PWM controller)
    # param: minX  - integer (The minimum value/angle for x-servo)
    # param: maxX  - integer (The maximum value/angle for x-servo)
    # param: minY  - integer (The minimum value/angle for y-servo)
    # param: maxY  - integer (The maximum value/angle for y-servo)
    assert type(portX) is int, "The port number for x-servo must be integer"
    assert type(portY) is int, "The port number for y-servo must be integer"
    assert type(minX)  is int, "The value for minimum X rotation must be integer"
    assert type(maxX)  is int, "The value for maximum X rotation must be integer"
    assert type(minY)  is int, "The value for minimum Y rotation must be integer"
    assert type(maxY)  is int, "The value for maximum Y rotation must be integer"
    self.pwm          = pwm
    self.portX        = portX
    self.portY        = portY
    self.minX         = minX
    self.maxX         = maxX
    self.minY         = minY
    self.maxY         = maxY
    self.span         = span
    self._setServos()

  def _setServos(self):
    self.servoX = Servo(self.pwm, self.portX, self.minX, self.maxX)
    self.servoY = Servo(self.pwm, self.portY, self.minY, self.maxY)

  def turnX(self, x):
    # param: x - integer (The value/angle at which to rotate the servo (0-100))
    self.servoX.turn(x)

  def turnY(self, y):
    # param: y - integer (The value/angle at which to rotate the servo (0-100))
    self.servoY.turn(y)

  def homeX(self):
    self.servoX.home()

  def homeY(self):
    self.servoY.home()

  def home(self):
    self.servoX.home()
    self.servoY.home()

  def increaseX(self):
    x = self.servoX.getValue() - self.span # Increase in value means decrease in x from POV
    self.servoX.turn(x)

  def decreaseX(self):
    x = self.servoX.getValue() + self.span # Decrease in value means increase in x from POV
    self.servoX.turn(x)

  def increaseY(self):
    y = self.servoY.getValue() + self.span
    self.servoY.turn(y)

  def decreaseY(self):
    y = self.servoY.getValue() - self.span
    self.servoY.turn(y)

if __name__ == "__main__":
  pass