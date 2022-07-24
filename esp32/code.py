import board
from microcontroller import watchdog as w
from watchdog import WatchDogMode
import circuitpython_schedule as schedule

from display import Display
from neokeys import NeoKeys
from net import Net
from env import Env

w.timeout=300 # Set a timeout of 5 minutes
w.mode = WatchDogMode.RESET

net = Net()
net.connect()
ntp_time = net.time()
mqtt = net.mqtt()

i2c_bus = board.I2C()
env = Env(i2c_bus)
neokeys = NeoKeys(i2c_bus)
display = Display(env, ntp_time)

#Global Mutable State
button_state = 2
last_ts = ntp_time.now()

def tick():
  # diff = last_ts.timestamp() - ntp_time.now().timestamp()
  diff = ntp_time.now().timestamp()
  neokeys.leds(button_state)
  display.show(button_state, diff)

schedule.every(10).seconds.do(tick)
schedule.every(1).minutes.do(mqtt.env_lambda(env))
schedule.every().hour.do(ntp_time.sync_time)

def set_state(new_state):
  global button_state
  if button_state != new_state:
    mqtt.button_event(new_state, button_state)
    last_ts = ntp_time.now()
    button_state = new_state
    tick()

tick()

while True:
  key = neokeys.scan()
  if key >= 0:
    set_state(key)
  schedule.run_pending()
