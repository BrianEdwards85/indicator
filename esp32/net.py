import wifi

from secrets import secrets
from ntp_time import NTP_Time
from mqtt import MQTT_Client

class Net:
    def connect(self):
      print("Connecting WiFi")
      wifi.radio.connect(secrets["ssid"], secrets["wifi_password"])
      print("My IP address is", wifi.radio.ipv4_address)
      self._mac = ':'.join([hex(i)[2:] for i in wifi.radio.mac_address])
      print("My MAC address is", self._mac)

      self.ntp_time = NTP_Time(wifi)
      self._mqtt = MQTT_Client(self._mac, self.ntp_time, wifi)
      self._mqtt.connect()

    def mqtt(self):
      return self._mqtt

    def time(self):
      return self.ntp_time

    def mac():
      return self._mac
