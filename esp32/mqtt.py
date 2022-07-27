import json
import socketpool
import ssl
import time
from microcontroller import watchdog as w
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_datetime import datetime

from consts import messages
from secrets import secrets

class MQTT_Client:
  def __init__(self, id, time, wifi):
    self.id = id
    self.time = time
    self.wifi = wifi
    self.mac = mac

  def payload(self, type, obj):
    base = {
      'type': type,
      'id': self.id,
      'timestamp': self.time.now().isoformat(),
    }
    base.update(obj)
    return base

  def send(self, type, obj):
    dt = self.time.now().timestamp()
    message = json.dumps(self.payload(type, obj))
    topic = "esp32s2/%s/%s" % (self.id.replace(':', '_'), type)
    print("Publish (%s): %s %f" % (topic, message, dt))
    self.mqtt_client.publish(topic, message)

  def connected(self, a, b, c, d):
    print("MQTT Connected")
    self.send('connected', {'ip': self.wifi.radio.ipv4_address})

  def disconnected(self, a, b, c):
    print("MQTT Disconnected")
    time.sleep(1)
    self.mqtt_client.connect()

  def connect(self):
    print("MQTT connect")
    self.pool = socketpool.SocketPool(self.wifi.radio)
    self.mqtt_client = MQTT.MQTT(
      broker=secrets["broker"],
      port=secrets["port"],
      username=secrets["mqtt_username"],
      password=secrets["mqtt_pw"],
      socket_pool=self.pool,
      ssl_context=ssl.create_default_context(),
      client_id="esp32s2_%s" % self.id.replace(':', '-'),
    )

    self.mqtt_client.on_connect = self.connected
    self.mqtt_client.on_disconnect = self.disconnected

    print("Attempting to connect to %s" % self.mqtt_client.broker)
    self.mqtt_client.connect()


  def button_event(self, new_state, old_state):
    payload = {
      'state': messages[new_state],
      'prev': messages[old_state],
    }
    self.send('button', payload)

  def env_event(self, env):
    w.feed()
    self.send('env', { 'temp': env.temp(), 'humidity': env.humidity() })

  def env_lambda(self, env):
    return lambda: self.env_event(env)


