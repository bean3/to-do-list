class Page():
	def __init__(self, plans, pg):

		#Page settings
		self.selectedPage = pg
		self.pageActivation = pg != 0
		self.rowsinPage = 10
		self.rowsinLastPage = len(plans) % self.rowsinPage

		#Calculating maximum page number
		calcPageNum = len(plans) // self.rowsinPage
		self.maxPageNum = calcPageNum if self.rowsinLastPage == 0 else calcPageNum + 1

	#Return true if page number is vaild(= Corresponding page exists)
	def isValid(self):
		return self.selectedPage in range(1, self.maxPageNum + 1)

	#Return true if pg is same with selected page number
	def isSelectedPage(self, pg):
		return self.selectedPage == pg

	#Return true if --pg option and specific page number is given
	def isActivated(self):
		return self.pageActivation == 1

