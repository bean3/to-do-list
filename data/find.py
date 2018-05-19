from detail import Detail

class Find():
	def __init__(self, db, key):
		self.cur = db.cur
		self.conn = db.conn
		self.findKey = key
		self.detail = Detail(db, None)

	def check(self):
		if(self.findKey == "%"):
			print("No matches found")
			return False

		else:
			self.cur.execute("select * from todo where what like '%" + self.findKey + "%'")
			self.resultRows = self.cur.fetchall()

			if self.resultRows:
				return True
			else:
				print("No matches found")
				return False

	def execute(self):

		while True:
			print(
				"\n",
				len(self.resultRows), " matches found\n"
				"\n"
				"No. | Description\n"
				"===================================================", sep = "")

			for row in self.resultRows:
				num = row[0]
				descr = row[1] if len(row[1]) <= 45 else row[1][:42] + "..."

				print(f"{num:3} | {descr:45}")

			print("===================================================")

			while True:
				if self.detail.check():
					self.detail.execute()
					input("Press Enter to continue...")
					self.detail.planNum = None
					break

				self.detail.planNum = None


