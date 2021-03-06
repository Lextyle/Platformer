import pygame
import pyautogui
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
class play_animation():
	def __init__(self, x, y, animation):
		self.animation = animation
		self.anim_count = 0
		self.x = x
		self.y = y
		self.frame_length = 2
	def draw(self, window):
		self.frame = self.animation[self.anim_count // self.frame_length]
		window.blit(self.frame, (self.x - self.frame.get_width() // 2, self.y - self.frame.get_height() // 2))
		self.anim_count += 1
from Player import *
from Platforms import *
from Cells import *
pygame.init()
# VARIABLES
window_width = pyautogui.size()[0]
window_height = pyautogui.size()[1]
window = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
player = Player(window_width // 2 - 6 // 2, window_height // 2 - 13 // 2)
left = right = up = False
music = pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)
block_break_sound = pygame.mixer.Sound("block_break.wav")
block_create_sound = pygame.mixer.Sound("block_create.wav")
level_1 = [
	"------------------------------------------------",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-          						                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"-                                              -",
	"------------------------------------------------"
]
platforms = []
y = 0
for line in level_1:
	x = 0
	for letter in line:
		if letter == "-":
			platform = Platform(x, y)
			platforms.append(platform)
		x += platform.image.get_width()
	y += platform.image.get_height()
clock = pygame.time.Clock()
create_block = break_block = False
cells = [Cell(20, 20, 40, 40, pygame.image.load("dirt.png")), Cell(60, 20, 40, 40, pygame.image.load("grass.png"))]
cells[0].activated = True
button_press_sound = pygame.mixer.Sound("button_pressed.wav")
animations = []
boom_animation = [pygame.transform.scale(pygame.image.load(r"boom_animation\1_frame.png"), (40, 40)), pygame.transform.scale(pygame.image.load(r"boom_animation\2_frame.png"), (40, 40)), pygame.transform.scale(pygame.image.load(r"boom_animation\3_frame.png"), (40, 40)), pygame.transform.scale(pygame.image.load(r"boom_animation\4_frame.png"), (40, 40)), pygame.transform.scale(pygame.image.load(r"boom_animation\5_frame.png"), (40, 40)), pygame.transform.scale(pygame.image.load(r"boom_animation\6_frame.png"), (40, 40)), pygame.transform.scale(pygame.image.load(r"boom_animation\7_frame.png"), (40, 40)), pygame.transform.scale(pygame.image.load(r"boom_animation\8_frame.png"), (40, 40)), pygame.transform.scale(pygame.image.load(r"boom_animation\9_frame.png"), (40, 40)), pygame.transform.scale(pygame.image.load(r"boom_animation\10_frame.png"), (40, 40)), pygame.transform.scale(pygame.image.load(r"boom_animation\11_frame.png"), (40, 40)), pygame.transform.scale(pygame.image.load(r"boom_animation\12_frame.png"), (40, 40)), pygame.transform.scale(pygame.image.load(r"boom_animation\13_frame.png"), (40, 40))]
# GAME LOOP
while True:
	clock.tick(60)
	mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
	window.fill((255, 255, 255))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				left = True
				right = False
			if event.key == pygame.K_d:
				right = True
				left = False
			if event.key == pygame.K_SPACE:
				up = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				left = False
			if event.key == pygame.K_d:
				right = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if not(mouse_pos_x in range(20, 20 + 40 * len(cells)) and mouse_pos_y in range(20, 60)):
				if event.button == 1:
					create_block = True
				if event.button == 3:
					break_block = True
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1 or event.button == 3:
				create_block = break_block = False
		for cell in cells:
			cell.update(event, cells)
	if create_block:
		x = mouse_pos_x - ((mouse_pos_x + platforms[0].rect.x * -1) % platforms[0].rect.width)
		y = mouse_pos_y - ((mouse_pos_y + platforms[0].rect.y * -1) % platforms[0].rect.height)
		platform = Platform(x, y)
		if cells[1].activated:
			platform.image = pygame.transform.scale(pygame.image.load("grass.png"), (40, 40))
		is_platform_in_platforms = False
		for platform_2 in platforms:
			if platform_2.rect.x == x and platform_2.rect.y == y:
				is_platform_in_platforms = True
				break
		if not is_platform_in_platforms:
			if (not player.rect.x in range((platform.rect.x + 1) - player.image.get_width(), platform.rect.x - 1 + platform.image.get_width())) or (not player.rect.y in range((platform.rect.y + 1) - player.image.get_height(), platform.rect.y - 1 + platform.image.get_height())):
				platforms.append(platform)
				block_create_sound.play()
	if break_block:
		x = mouse_pos_x - ((mouse_pos_x + platforms[0].rect.x * -1) % platforms[0].rect.width)
		y = mouse_pos_y - ((mouse_pos_y + platforms[0].rect.y * -1) % platforms[0].rect.height)
		platform = Platform(x, y)
		for platform_2 in platforms:
			if platform_2.rect.x == x and platform_2.rect.y == y:
				platforms.pop(platforms.index(platform_2))
				block_break_sound.play()
				animations.append(play_animation(platform_2.rect.x + platform_2.rect.width // 2, platform_2.rect.y + platform_2.rect.height // 2, boom_animation))
				break
	player.update(left, right, up, platforms, animations)
	for platform in platforms:
		platform.draw(window)
	for animation in animations:
		if animation.anim_count == len(animation.animation) * animation.frame_length:
			animations.pop(animations.index(animation))
			continue
		animation.draw(window)
	player.draw(window)
	for cell in cells:
		cell.draw(window)
	pygame.display.flip()
	up = False