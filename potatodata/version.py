class Version():
	def __init__(self):
		self.version = '1.0.8'

	def check(self):
		return True

	def execute(self):
		print(self.version)
