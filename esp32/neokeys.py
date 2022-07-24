from adafruit_neokey.neokey1x4 import NeoKey1x4
from consts import colors

class NeoKeys:
  def __init__(self, i2c_bus):
    self.neokey = NeoKey1x4(i2c_bus, addr=0x30)

  def leds(self, state):
    for x in range(4):
      if x == state:
        self.neokey.pixels[state] = colors[state]
      else:
        self.neokey.pixels[x] = 0x0

  def scan(self):
    for i in range(4):
      if self.neokey[i]:
        return i
    return -1
