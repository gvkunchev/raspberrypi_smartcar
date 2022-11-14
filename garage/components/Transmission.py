#!/usr/bin/python
from hardware.Motor import Motor

class Transmission(object):
  "Transmission of the car. It drives the two motors and change their speed."

  def __init__(self, pwm, motor1PinFwd, motor1PinBwd, motor1PinSpeed, motor2PinFwd, motor2PinBwd, motor2PinSpeed):
    # param: pwm            - object  (The PWM controller that controls the speed of the motor)
    # param: motor1PinFwd   - integer (The pin on Pi that controls the fwd motion for motor 1)
    # param: motor1PinBwd   - integer (The pin on Pi that controls the bwd motion for motor 1)
    # param: motor1PinSpeed - integer (The pin on the PWM controller that controls the speed for motor 1)
    # param: motor2PinFwd   - integer (The pin on Pi that controls the fwd motion for motor 2)
    # param: motor2PinBwd   - integer (The pin on Pi that controls the bwd motion for motor 2)
    # param: motor2PinSpeed - integer (The pin on the PWM controller that controls the speed for motor 2)
    assert type(motor1PinFwd)   is int, "The pin number for forward on motor 1 must be integer"
    assert type(motor1PinBwd)   is int, "The pin number for backword on motor 1 must be integer"
    assert type(motor1PinSpeed) is int, "The pin number for speed on motor 1 must be integer"
    assert type(motor2PinFwd)   is int, "The pin number for forward on motor 2 must be integer"
    assert type(motor2PinBwd)   is int, "The pin number for backword on motor 2 must be integer"
    assert type(motor2PinSpeed) is int, "The pin number for speed on motor 2 must be integer"
    self.motor1 = Motor(pwm, motor1PinFwd, motor1PinBwd, motor1PinSpeed)
    self.motor2 = Motor(pwm, motor2PinFwd, motor2PinBwd, motor2PinSpeed)

  def fwd(self):
    self.motor1.fwd()
    self.motor2.fwd()

  def bwd(self):
    self.motor1.bwd()
    self.motor2.bwd()

  def stop(self):
    self.motor1.stop()
    self.motor2.stop()

  def setSpeed(self, speed):
    # param: speed - integer (The speed at which the transmission should operate (0-100))
    assert type(speed) is int, "The value for speed must be integer"
    self.motor1.setSpeed(speed)
    self.motor2.setSpeed(speed)

if __name__ == "__main__":
  pass