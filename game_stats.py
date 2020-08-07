class GameStats:
	def __init__(self, ai_game):
		self.settings = ai_game.settings
		self.reset_stats()
		#start game in inactive state
		self.game_active = False
		self.high_score = 0
		self.level = 1

	def reset_stats(self):
		self.ships_left = self.settings.ship_limit
		self.score = 0

	def update_high_score(self):
		file_name = "high_score.txt"
		with open(file_name,'w+') as file_object:
			highscore = file_object.readlines()

			high_score=''
			for hs in highscore:
				high_score += hs
			if self.score > int(high_score):
				file_object.write(f'{int(self.score)}')
			else:
				file_object.write('0')

	def read_high_score(self):
		file_name = "high_score.txt"
		with open(file_name,'r') as file_object:
			highscore = file_object.readlines()

		high_score = ''
		for hs in highscore:
			high_score += hs
		return int(high_score)
		
