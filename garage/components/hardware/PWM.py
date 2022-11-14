#!/usr/bin/python
import smbus
import math
import time
import RPi.GPIO as GPIO

class PWM(object):
  "PCA9685 16-Channel 12-Bit I2C BUS PWM Driver in Pi B+"
  
  _frequency      = 60

  _MODE1          = 0x00
  _MODE2          = 0x01
  _SUBADR1        = 0x02
  _SUBADR2        = 0x03
  _SUBADR3        = 0x04
  _PRESCALE       = 0xFE
  _LED0_ON_L      = 0x06
  _LED0_ON_H      = 0x07
  _LED0_OFF_L     = 0x08
  _LED0_OFF_H     = 0x09
  _ALL_LED_ON_L   = 0xFA
  _ALL_LED_ON_H   = 0xFB
  _ALL_LED_OFF_L  = 0xFC
  _ALL_LED_OFF_H  = 0xFD
  _RESTART        = 0x80
  _SLEEP          = 0x10
  _ALLCALL        = 0x01
  _INVRT          = 0x10
  _OUTDRV         = 0x04
  
  def __init__(self, bus_number=1, address=0x40):
    self.bus_number = bus_number
    self.address    = address
    self._assignBus()
    self.setAllvalue(0, 0)
    self._initMode1()
    self._initMode2()
    time.sleep(0.005)
    self._disableSleepMode()
    time.sleep(0.005)
    self._setFrequency(self._frequency)
  
  def _initMode1(self):
    self._writeByteData(self._MODE1, self._ALLCALL)
  
  def _initMode2(self):
    self._writeByteData(self._MODE2, self._OUTDRV)

  def _assignBus(self):
    self.bus = smbus.SMBus(self.bus_number)
  
  def _writeByteData(self, reg, value):
    self.bus.write_byte_data(self.address, reg, value)

  def _readByteData(self, reg):
    results = self.bus.read_byte_data(self.address, reg)
    return results
  
  def _enableRestart(self):
    old_mode = self._readByteData(self._MODE1)
    new_mode = old_mode | self._RESTART
    self._writeByteData(self._MODE1, new_mode)
    
  def _disableRestart(self):
    old_mode = self._readByteData(self._MODE1)
    new_mode = old_mode & ~self._RESTART
    self._writeByteData(self._MODE1, new_mode)
  
  def _enableSleepMode(self):
    old_mode = self._readByteData(self._MODE1)
    new_mode = old_mode | self._SLEEP
    self._writeByteData(self._MODE1, new_mode)
  
  def _disableSleepMode(self):
    old_mode = self._readByteData(self._MODE1)
    new_mode = old_mode & ~self._SLEEP
    self._writeByteData(self._MODE1, new_mode)
  
  def _getMode1(self):
    return self._readByteData(self._MODE1)
  
  def _setMode1(self, mode):
    return self._writeByteData(self._MODE1, mode)
  
  def _calculateFrequency(self, freq):
    prescale_value = 25000000.0
    prescale_value /= 4096.0
    prescale_value /= float(freq)
    prescale_value -= 1.0
    return int(math.floor(round(prescale_value)))

  def _setFrequency(self, freq):
    old_mode = self._getMode1()
    self._disableRestart()
    self._enableSleepMode()
    self._writeByteData(self._PRESCALE, self._calculateFrequency(freq))
    self._setMode1(old_mode)
    time.sleep(0.005)
    self._enableRestart()
  
  
  def setValue(self, channel, on, off):
    self._writeByteData(self._LED0_ON_L+4*channel, on & 0xFF)
    self._writeByteData(self._LED0_ON_H+4*channel, on >> 8)
    self._writeByteData(self._LED0_OFF_L+4*channel, off & 0xFF)
    self._writeByteData(self._LED0_OFF_H+4*channel, off >> 8)

  def setAllvalue(self, on, off):
    self._writeByteData(self._ALL_LED_ON_L, on & 0xFF)
    self._writeByteData(self._ALL_LED_ON_H, on >> 8)
    self._writeByteData(self._ALL_LED_OFF_L, off & 0xFF)
    self._writeByteData(self._ALL_LED_OFF_H, off >> 8)

if __name__ == "__main__":
  pass
