from pygame.image import load as load_image
from pygame.transform import scale as scale_image
class Platform():
	def __init__(self, x, y):
		self.image = scale_image(load_image("dirt.png"), (40, 40))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	def draw(self, window):
		window.blit(self.image, (self.rect.x, self.rect.y))