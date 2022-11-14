#!/usr/bin/python

class Driver(object):
  "Driver for a Car - receives string command and sends them to the Car"

  commandMap = {
    'cam_up'           : 'self.car.camIncreaseY()',
    'cam_down'         : 'self.car.camDecreaseY()',
    'cam_left'         : 'self.car.camDecreaseX()',
    'cam_right'        : 'self.car.camIncreaseX()',
    'cam_home'         : 'self.car.camHome()',
    'move_fwd'         : 'self.car.moveFwd()',
    'move_bwd'         : 'self.car.moveBwd()',
    'move_stop'        : 'self.car.stopMoving()',
    'steer_left'       : 'self.car.turnLeft()',
    'steer_right'      : 'self.car.turnRight()',
    'steer_home'       : 'self.car.turnHome()',
    'init'             : 'self.car.init()'
  }

  def __init__(self, car):
    # param: car - object (The car object that the driver should operate)
    self.car = car

  def executeCommand(self, command):
    # param: command - string (The command to be executed by the Car)
    if command in self.commandMap.keys():
      eval(self.commandMap[command])
    elif 'speed_' in command:
      speed = command.strip('speed_')
      speed = int(speed)
      self.car.setSpeed(speed)
    elif 'turn_' in command:
      turn = command.strip('turn_')
      turn = int(turn)
      self.car.turn(turn)
    else:
      raise Exception("Unknown command.")

if __name__ == "__main__":
  pass