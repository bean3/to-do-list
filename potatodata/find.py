from .detail import Detail

class Find():
	def __init__(self, db, what, month):
		self.cur = db.cur
		self.conn = db.conn
		self.detail = Detail(db, None)

		self.findKey = what if what else month
		if self.findKey == what:
			self.sql = "select * from todo where what like '%" + self.findKey + "%'"
			self.searchTopic = "Description"
		else:
			self.sql = "SELECT * FROM todo WHERE due LIKE '%'||'-"+format(self.findKey, '02')+"'||'%'"
			self.searchTopic = "Due"

	def check(self):
		if(self.findKey == "%"):
			print("\nNo matches found\n")
			return False

		else:
			self.cur.execute(self.sql)
			self.resultRows = self.cur.fetchall()

			if self.resultRows:
				return True
			else:
				print("\nNo matches found\n")
				return False

	def get_item(self, row):
		descr = row[1] if len(row[1]) <= 45 else row[1][:42] + "..."
		due = row[2]

		self.item = {
		'Description': descr,
		'Due': due
		}.get(self.searchTopic)

		return self.item

	def execute(self):
		while True:
			print(
				"\n",
				len(self.resultRows), " matches found\n"
				"\n"
				"No. | " + self.searchTopic + "\n"
				"===================================================", sep = "")

			for row in self.resultRows:
				num = row[0]

				print(f"{num:3} | " + self.get_item(row))

			print("===================================================")

			while True:
				if self.detail.check():
					self.detail.execute()
					input("Press Enter to continue...")
					self.detail.planNum = None
					break

				self.detail.planNum = None


