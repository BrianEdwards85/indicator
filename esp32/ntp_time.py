import rtc
import socketpool
import time
import adafruit_ntp
from adafruit_datetime import datetime
import circuitpython_schedule as schedule

class NTP_Time:
  def sync_time(self):
    print('Sync time')
    self.rtc.datetime = self.ntp.datetime

  def __init__(self, wifi):
    self.pool = socketpool.SocketPool(wifi.radio)
    self.ntp = adafruit_ntp.NTP(self.pool, tz_offset=-5)
    self.rtc = rtc.RTC()
    self.sync_time()

  def now(self):
    dt = time.localtime()
    return datetime(
      dt.tm_year, 
      dt.tm_mon,
      dt.tm_mday,
      dt.tm_hour,
      dt.tm_min,
      dt.tm_sec,
    )