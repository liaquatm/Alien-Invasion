class Settings:
	def __init__(self):
		#Screen settings
		self.screen_width=1300
		self.screen_height=700
		self.bg_color=(230,230,230)
		#ship settings
		self.ship_limit = 3
		#bullet settings
		self.bullet_width=3
		self.bullet_height=15
		self.bullet_color=(60,60,60)
		self.bullets_allowed=5
		#alien settings
		self.fleet_drop_speed=10	
		#game speed up rate
		self.speedup_scale = 1.1
		self.initialize_dynamic_settings()
		#points increase rate
		self.score_scale = 1.5

	def initialize_dynamic_settings(self):
		self.ship_speed=1.5
		self.bullet_speed=1.5
		self.alien_speed=1
		#to change fleet direction
		self.fleet_direction=1
		#scoring
		self.alien_points = 50

	def increase_speed(self):
		"""increase speed settings andalien point values"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
		print(self.alien_points)
		self.bullets_allowed += 1