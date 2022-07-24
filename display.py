
import board
import displayio
import terminalio
from adafruit_display_text import bitmap_label

from consts import messages, colors

class Display:
  def __init__(self, env, time):
    self.env = env
    self.time = time

  def env_area(self):
    text_area = bitmap_label.Label(
      terminalio.FONT, 
      scale=2,
      text="%0.1f F  %0.1f %%" % (self.env.temp(), self.env.humidity())
    )
    text_area.x = 10
    text_area.y = 60

    return text_area

  def dt_area(self):
    dt = self.time.now()
    text_area = bitmap_label.Label(
      terminalio.FONT,
      text=dt.isoformat(),
      scale=2
    )
    text_area.x = 10
    text_area.y = 40

    return text_area

  def state_area(self, state):
    text_area = bitmap_label.Label(
      terminalio.FONT,
      text=messages[state],
      scale=3,
      color=colors[state]
    )
    text_area.x = 10
    text_area.y = 10

    return text_area

  def diff_area(self, diff):
    text_area = bitmap_label.Label(
      terminalio.FONT,
      text="%f" % diff,
      scale=3,
    )
    text_area.x = 10
    text_area.y = 90

    return text_area


  def show(self, state, diff):
    main_group = displayio.Group()
    main_group.append(self.dt_area())
    main_group.append(self.state_area(state))
    main_group.append(self.env_area())
#    main_group.append(self.diff_area(diff))

    board.DISPLAY.show(main_group)