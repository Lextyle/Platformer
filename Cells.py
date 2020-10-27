from pygame.draw import rect as draw_rect
from pygame import Surface
from pygame.transform import scale as scale_image
from pygame import MOUSEBUTTONDOWN
from pygame.font import Font
from pygame.mixer import Sound
button_press_sound = Sound("button_pressed.wav")
class Cell():
  def __init__(self, x, y, width, height, block_image):
    self.x = x
    self.y = y
    self.activated = False
    self.small_block_image = scale_image(block_image, (20, 20))
    self.image = Surface((width, height))
    self.image.fill((139,69,19))
    self.image.set_alpha(60)
  def update(self, event, cells):
    if event.type == MOUSEBUTTONDOWN:
      if event.button == 1:
        if event.pos[0] in range(self.x, self.x + self.image.get_width()) and event.pos[1] in range(self.y, self.y + self.image.get_height()):
          button_press_sound.play()
          self.activated = True
          for cell in cells:
            if cell != self:
              cell.activated = False
  def draw(self, window):
    window.blit(self.image, (self.x, self.y))
    if self.activated:
      draw_rect(window, (0, 0, 0), (self.x, self.y, self.image.get_width(), self.image.get_height()), 2)
    else:
      draw_rect(window, (150, 150, 150), (self.x, self.y, self.image.get_width(), self.image.get_height()), 2)
    window.blit(self.small_block_image, ((self.x + self.image.get_width() // 2) - self.small_block_image.get_width() // 2, (self.y + self.image.get_height() // 2) - self.small_block_image.get_height() // 2))