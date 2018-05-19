class Category():
	def __init__(self, db):
		sql = "select category from todo where 1"
		db.cur.execute(sql)
		self.allCats = db.cur.fetchall()

		#No duplicate category, but !UNORDERED!
		self.existingCats = {cat[0] for cat in self.allCats}

	#Return true if there is at least 1 category
	def isEmpty(self):
		if self.allCats:
			return False
		else:
			print("Please make a plan by using --mk [descr.] [due] [cat.] first.")
			return True

	#Return set of categories
	def get(self):
		return self.existingCats

	#Return true if it exists
	def check(self, cat):
		if cat in self.existingCats:
			return True
		else:
			print("\nInvaild category :(\n")
			return False

	#Print all categories
	#[cat1] [cat2] [cat3] ...
	def show(self):
		print()
		for cat in self.existingCats:
			print("[{}]".format(cat), end=" ")
