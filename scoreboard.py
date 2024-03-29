import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
	def __init__(self, ai_game):
		"""initialize scorekeeping attributes"""
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats
		#font settings for scoreboard
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None, 48)
		#prepare initial score image
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_level(self):
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str, True,
			self.text_color, self.settings.bg_color)
		self.level_rect = self.level_image.get_rect()
		self.level_rect.left = self.screen_rect.left + 20
		self.level_rect.top = self.score_rect.top

	def prep_ships(self):
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_game)
			ship.rect.top = 10
			ship.rect.x = self.level_rect.right + 10 + ship_number * ship.rect.width
			self.ships.add(ship)

	def prep_score(self):
		"""turn score into a rendered image"""
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True,
			self.text_color, self.settings.bg_color)
		#display score at top right of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		"""turn the high score into a rendered image"""
		high_score = round(self.stats.high_score, -1)
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str,
			True, self.text_color, self.settings.bg_color)
		#center the high score on top of the screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def check_high_score(self):
		"""check to seeif there's a new high score"""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()

	def show_score(self):
		"""draw score,level and ships on the screen"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)