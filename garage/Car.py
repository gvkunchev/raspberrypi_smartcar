#!/usr/bin/python
import RPi.GPIO as GPIO
from components.Periscope import Periscope
from components.Transmission import Transmission
from components.Wheel import Wheel
from components.hardware.PWM import PWM


class Car(object):
  "Car object that will control all pieces on board"

  motorLpinFwd         = 11   # Pin for forward movement for the left motor on the Pi
  motorLpinBwd         = 12   # Pin for backword movement for the left motor on the Pi
  motorLpinSpd         = 5    # Pin for speed control of the left motor on the PWM controller
  motorRpinFwd         = 15   # Pin for forward movement for the right motor on the Pi
  motorRpinBwd         = 13   # Pin for backword movement for the right motor on the Pi
  motorRpinSpd         = 4    # Pin for speed control of the right motor on the PWM controller

  camServoPortX        = 14   # Port on the PWM controller for the X-controlling servo of the periscope
  camServoPortY        = 15   # Port on the PWM controller for the Y-controlling servo of the periscope
  steerServoPort       = 0    # Port for the steering servo on the PWM controller

  camServoMinX         = 270  # The minimum angle for rotation of the x-servo on the periscope
  camServoMaxX         = 620  # The maximum angle for rotation of the x-servo on the periscope
  camServoMinY         = 200  # The minimum angle for rotation of the y-servo on the periscope
  camServoMaxY         = 700  # The maximum angle for rotation of the y-servo on the periscope
  steerServoMin        = 360  # Minimum value for the steering servo
  steerServoMax        = 510  # Maximum value for the steering servo

  camSpan              = 5    # The value at which to turn the camera at a single turn request

  def __init__(self):
    self.pwm          = PWM()
    self.periscope    = Periscope(self.pwm,
                                  self.camServoPortX,
                                  self.camServoPortY,
                                  self.camServoMinX,
                                  self.camServoMaxX,
                                  self.camServoMinY,
                                  self.camServoMaxY,
                                  self.camSpan)
    self.transmission = Transmission(self.pwm,
                                     self.motorLpinFwd,
                                     self.motorLpinBwd,
                                     self.motorLpinSpd,
                                     self.motorRpinFwd,
                                     self.motorRpinBwd,
                                     self.motorRpinSpd)
    self.wheel        = Wheel(self.pwm,
                              self.steerServoPort,
                              self.steerServoMin,
                              self.steerServoMax)

  def init(self):
    self.transmission.stop()
    self.wheel.home()
    self.transmission.setSpeed(50)

  def moveFwd(self):
    self.transmission.fwd()

  def moveBwd(self):
    self.transmission.bwd()

  def stopMoving(self):
    self.transmission.stop()

  def setSpeed(self, speed):
    # param: speed - integer (The speed which need to be set (1-100)
    self.transmission.setSpeed(speed)
    
  def turnLeft(self):
    self.wheel.turnLeft()

  def turnRight(self):
    self.wheel.turnRight()

  def turn(self, value):
    # param: value - integer (The angle at which to turn the steer)
    self.wheel.turn(value)

  def turnHome(self):
    self.wheel.home()
  
  def camHome(self):
    self.periscope.home()

  def camIncreaseX(self):
    self.periscope.increaseX()

  def camDecreaseX(self):
    self.periscope.decreaseX()

  def camIncreaseY(self):
    self.periscope.increaseY()

  def camDecreaseY(self):
    self.periscope.decreaseY()

if __name__ == "__main__":
  pass
