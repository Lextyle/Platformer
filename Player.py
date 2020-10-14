from pygame.image import load as load_image
from pygame.transform import scale as scale_image
from pygame.transform import flip as flip_image
from pygame.sprite import collide_rect
from pygame import mixer
mixer.pre_init(44100, -16, 2, 512)
MOVE_SPEED = 1
JUMP_POWER = 20
GRAVITY = 0.6
class Player():
	def __init__(self, x, y):
		self.image = scale_image(load_image("player.png"), (6 * 3, 13 * 3))
		self.x_vel = 0
		self.y_vel = 0
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.on_ground = False
		self.jump_sound = mixer.Sound("jump.wav")
		self.jump_count = 0
		self.scroll = [0, 0]
	def update(self, left, right, up, platforms):
		if left:
			self.image = flip_image(scale_image(load_image(r"player.png"), (self.rect.width, self.rect.height)), 1, 0)
			self.x_vel -= MOVE_SPEED
		elif right:
			self.image = scale_image(load_image(r"player.png"), (self.rect.width, self.rect.height))
			self.x_vel += MOVE_SPEED
		else:
			if self.x_vel > 0:
				self.x_vel -= MOVE_SPEED
			if self.x_vel < 0:
				self.x_vel += MOVE_SPEED
		if up:
			if self.on_ground or self.jump_count == 1:
				self.jump_sound.play()
				self.y_vel = JUMP_POWER * -1
				self.jump_count += 1
		if not self.on_ground:
			self.y_vel += GRAVITY
		self.on_ground = False
		self.scroll[0] = self.x_vel // 3
		self.scroll[1] = self.y_vel // 3
		self.move(platforms)
	def move(self, platforms):
		for platform in platforms:
			platform.rect.x -= self.scroll[0]
		for platform in platforms:
			if collide_rect(self, platform):
				for platform in platforms:
					platform.rect.x += self.scroll[0]
				self.x_vel = 0
				self.scroll[0] = 0
				break
		for platform in platforms:
			platform.rect.y -= self.scroll[1]
		for platform in platforms:
			if collide_rect(self, platform):
				if self.y_vel > 0:
					self.on_ground = True
					self.jump_count = 0
				if self.y_vel < 0:
					self.y_vel = 0
				for platform in platforms:
					platform.rect.y += self.scroll[1]
				self.scroll[1] = 0
				break
	def draw(self, window):
		window.blit(self.image, (self.rect.x, self.rect.y))