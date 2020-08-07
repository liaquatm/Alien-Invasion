import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	def __init__(self):
		pygame.init()
		self.settings=Settings()
		self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		self.settings.screen_width=self.screen.get_rect().width
		self.settings.screen_height=self.screen.get_rect().height
		pygame.display.set_caption("Star Defender 2.0")
		self.stats=GameStats(self)
		self.sb=Scoreboard(self)
		self.ship=Ship(self)
		self.bullets=pygame.sprite.Group()
		self.aliens=pygame.sprite.Group()
		self._create_fleet()
		self.play_button = Button(self, "Play")

	def run_game(self):

		while True:
			self._check_events()
			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			self._update_screen()


	def _check_events(self):
		"""respond to key presses and events"""
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				sys.exit()
			elif event.type==pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
			elif event.type==pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type==pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_keydown_events(self,event):
		if event.key==pygame.K_RIGHT:
			self.ship.moving_right=True
		elif event.key==pygame.K_LEFT:
			self.ship.moving_left=True
		elif event.key==pygame.K_q:
			sys.exit()
		elif event.key==pygame.K_SPACE:
			self._fire_bullet()
		elif event.key==pygame.K_p:
			self._start_game()

	def _check_keyup_events(self,event):
		if event.key==pygame.K_RIGHT:
			self.ship.moving_right=False
		elif event.key==pygame.K_LEFT:
			self.ship.moving_left=False			

	def _fire_bullet(self): # used in _check_keydown-events
		"""Create a new bullet and add it the bullets group"""
		if len(self.bullets)<self.settings.bullets_allowed:
			new_bullet=Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		self.bullets.update()
		for bullet in self.bullets.copy():
			if bullet.rect.bottom<=0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		#remove any bullets and aliens that have collided
		collisions=pygame.sprite.groupcollide(self.bullets,
			self.aliens,True,True)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()
		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			#increase level
			self.stats.level += 1
			self.sb.prep_level()

	def _create_fleet(self):
		#make an alien
		alien=Alien(self)
		alien_width, alien_height=alien.rect.size
		available_space_x=self.settings.screen_width-(2*alien_width)
		number_aliens_x=available_space_x//(2*alien_width)

		ship_height=self.ship.rect.height
		available_space_y=(self.settings.screen_height-(3*alien_height)-ship_height)
		number_rows=available_space_y//(2*alien_height)

		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number,row_number)

	def _create_alien(self,alien_number,row_number):
		alien=Alien(self)
		alien_width, alien_height=alien.rect.size
		alien.x=alien_width+2*alien_width*alien_number
		alien.rect.x=alien.x
		alien.rect.y=alien_height+2*alien_height*row_number
		self.aliens.add(alien)

	def _update_aliens(self):
		self._check_fleet_edges()
		self.aliens.update()
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		#look for aliens hittingthe bottmof the screen
		self._check_aliens_bottom()

	def _check_fleet_edges(self):
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		for alien in self.aliens.sprites():
			alien.rect.y+=self.settings.fleet_drop_speed
		self.settings.fleet_direction*=-1

	def _update_screen(self):
		"""Update images on the screen, and  flip to new screen"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		#draw score info
		self.sb.show_score()
		#draw play button when game inactive
		if not self.stats.game_active:
			self.play_button.draw_button()
		pygame.display.flip()

	def _ship_hit(self):
		"""respond to ship hit by aliens"""
		if self.stats.ships_left>0:
			#decrement ships
			self.stats.ships_left -= 1
			self.sb.prep_ships()
			#get rid or remaining alines and bullets
			self.aliens.empty()
			self.bullets.empty()
			#create new alien fleet and center ship
			self._create_fleet()
			self.ship.center_ship()
			#pause
			sleep(0.5)
		else:
			self.stats.game_active=False
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		"""check if aliens reach the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				self._ship_hit()
				break

	def _check_play_button(self, mouse_pos):
		"""start a new game when player clicks play button"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self._start_game()

	def _start_game(self):
		#reset game stats
		self.stats.reset_stats()
		self.stats.game_active = True
		self.sb.prep_score()
		self.sb.prep_level()
		self.sb.prep_ships()
		#get rid of aliens and bullets
		self.aliens.empty()
		self.bullets.empty()
		#create new fleet of aliens and center ship
		self._create_fleet()
		self.ship.center_ship()
		#resetting speed
		self.settings.initialize_dynamic_settings()
		
		pygame.mouse.set_visible(False)


if __name__=='__main__':
	ai=AlienInvasion()
	ai.run_game()