try:
	import pygame
except:
	from os import system
	system("pip install pygame")
try:
	import pyautogui
except:
	from os import system
	system("pip install pyautogui")
class play_boom_animation():
	def __init__(self, x, y):
		self.animation = [pygame.image.load(r"boom_animation\1_frame.png"), pygame.image.load(r"boom_animation\2_frame.png"), pygame.image.load(r"boom_animation\3_frame.png"), pygame.image.load(r"boom_animation\4_frame.png"), pygame.image.load(r"boom_animation\5_frame.png")]
		self.anim_count = 0
		self.x = x
		self.y = y
	def draw(self, window):
		self.frame = self.animation[self.anim_count // 2]
		window.blit(self.frame, (self.x - self.frame.get_width() // 2, self.y - self.frame.get_height() // 2))
		self.anim_count += 1
from Player import *
from Platforms import *
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
all_versions_of_level = [platforms]
create_block = break_block = False
block_cell_side = 40
dirt_cell = pygame.Surface((block_cell_side, block_cell_side))
grass_cell = pygame.Surface((block_cell_side, block_cell_side))
dirt_cell_activated = True
grass_cell_activated = False
num_of_blocks = 2
dirt_cell_pos = (window_width // 2 - (block_cell_side * num_of_blocks) // 2, window_height - 90)
grass_cell_pos = (dirt_cell_pos[0] + block_cell_side, dirt_cell_pos[1])
dirt_cell.fill((139,69,19))
grass_cell.fill((139,69,19))
dirt_cell.set_alpha(60)
grass_cell.set_alpha(60)
dirt_small_image = pygame.transform.scale(pygame.image.load("dirt.png"), (block_cell_side // 2, block_cell_side // 2))
grass_small_image = pygame.transform.scale(pygame.image.load("grass.png"), (block_cell_side // 2, block_cell_side // 2))
button_press_sound = pygame.mixer.Sound("button_pressed.wav")
boom_animations = []
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
			if event.key == pygame.K_z and not (create_block or break_block):
				if len(all_versions_of_level) > 1:
					platforms = all_versions_of_level[-1]
					all_versions_of_level.pop(-1)
			if not (dirt_cell_activated) and event.key == pygame.K_1:
				dirt_cell_activated = True
				grass_cell_activated = False
				button_press_sound.play()
			if not (grass_cell_activated) and event.key == pygame.K_2:
				dirt_cell_activated = False
				grass_cell_activated = True
				button_press_sound.play()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if not (dirt_cell_activated) and mouse_pos_x in range(dirt_cell_pos[0], dirt_cell_pos[0] + dirt_cell.get_width()) and mouse_pos_y in range(dirt_cell_pos[1], dirt_cell_pos[1] + dirt_cell.get_height()):
					dirt_cell_activated = True
					grass_cell_activated = False
					button_press_sound.play()
				if not (grass_cell_activated) and mouse_pos_x in range(grass_cell_pos[0], grass_cell_pos[0] + grass_cell.get_width()) and mouse_pos_y in range(grass_cell_pos[1], grass_cell_pos[1] + grass_cell.get_height()):
					dirt_cell_activated = False
					grass_cell_activated = True
					button_press_sound.play()
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				left = False
			if event.key == pygame.K_d:
				right = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if not(mouse_pos_x in range(dirt_cell_pos[0], dirt_cell_pos[0] + block_cell_side * num_of_blocks)) or not(mouse_pos_y in range(dirt_cell_pos[1], dirt_cell_pos[1] + dirt_cell.get_height())):
				if event.button == 1:
					all_versions_of_level.append(platforms.copy())
					create_block = True
				if event.button == 3:
					all_versions_of_level.append(platforms.copy())
					break_block = True
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button != 2:
				create_block = break_block = False
		if create_block:
			x = mouse_pos_x - ((mouse_pos_x + platforms[0].rect.x * -1) % platforms[0].rect.width)
			y = mouse_pos_y - ((mouse_pos_y + platforms[0].rect.y * -1) % platforms[0].rect.height)
			platform = Platform(x, y)
			if grass_cell_activated:
				platform.image = pygame.transform.scale(pygame.image.load("grass.png"), (40, 40))
			is_platform_in_platforms = False
			for platform_2 in platforms:
				if platform_2.rect.x == x and platform_2.rect.y == y:
					is_platform_in_platforms = True
					break
			if not is_platform_in_platforms:
				if not (player.rect.x in range((platform.rect.x + 1) - player.image.get_width(), platform.rect.x - 1 + platform.image.get_width())) or not (player.rect.y in range((platform.rect.y + 1) - player.image.get_height(), platform.rect.y - 1 + platform.image.get_height())):
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
					boom_animations.append(play_boom_animation(platform_2.rect.x + platform_2.rect.width // 2, platform_2.rect.y + platform_2.rect.height // 2))
					break
	player.update(left, right, up, platforms)
	for platform in platforms:
		platform.draw(window)
	for boom_animation in boom_animations:
		if boom_animation.anim_count == len(boom_animation.animation) * 2:
			boom_animations.pop(boom_animations.index(boom_animation))
			continue
		boom_animation.draw(window)
	player.draw(window)
	window.blit(dirt_small_image, ((dirt_cell_pos[0] + dirt_cell.get_width() // 2) - dirt_small_image.get_width() // 2, (dirt_cell_pos[1] + dirt_cell.get_height() // 2) - dirt_small_image.get_height() // 2))
	window.blit(grass_small_image, ((grass_cell_pos[0] + grass_cell.get_width() // 2) - grass_small_image.get_width() // 2, (grass_cell_pos[1] + grass_cell.get_height() // 2)  - grass_small_image.get_height() // 2))
	window.blit(dirt_cell, dirt_cell_pos)
	window.blit(grass_cell, grass_cell_pos)
	if dirt_cell_activated:
		pygame.draw.rect(window, (0, 0, 0), (dirt_cell_pos[0], dirt_cell_pos[1], block_cell_side, block_cell_side), 2)
	else:
		pygame.draw.rect(window, (150, 150, 150), (dirt_cell_pos[0], dirt_cell_pos[1], block_cell_side, block_cell_side), 2)
	if grass_cell_activated:
		pygame.draw.rect(window, (0, 0, 0), (grass_cell_pos[0], grass_cell_pos[1], block_cell_side, block_cell_side), 2)
	else:
		pygame.draw.rect(window, (150, 150, 150), (grass_cell_pos[0], grass_cell_pos[1], block_cell_side, block_cell_side), 2)
	pygame.display.update()
	up = False