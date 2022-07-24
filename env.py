from adafruit_bme280 import basic as adafruit_bme280

class Env:
  def __init__(self, i2c):
    self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

  def temp(self):
    return (self.bme280.temperature * 9/5) + 32

  def humidity(self):
    return self.bme280.humidity
