import re
from datetime import datetime

class Make():
	def __init__(self, db, input_data):
		self.inputData = input_data
		self.cur = db.cur
		self.conn = db.conn

		#Format settings
		self.inputFormat1 = r"(\d{4})[-](\d{2})[-](\d{2})[/](\d{2})[:](\d{2})"
		self.inputFormat2 = r"(\d{4})[-](\d{2})[-](\d{2})\s(\d{2})[:](\d{2})"
		self.inputLength = 16

	#Check whether the input satisfies the format
	def check(self):
		inputDue = self.inputData[1]
		regular = re.compile(self.inputFormat1)
		while True:
			if len(inputDue) != self.inputLength:
				print("Please type in the right format : YYYY-MM-DD/HH:MM")
				return False
			match = regular.match(inputDue)
			if match == None:
				print("Please type in the right format : YYYY-MM-DD/HH:MM")
				return False
			else:
				break
		timeNow = datetime.now()
		regular2 = re.compile(self.inputFormat2)
		match2 = regular2.match(str(timeNow))
		inputDue = regular.match(self.inputData[1])
		for i in range(1, 6):
			if int(inputDue.group(i)) < int(match2.group(i)):
				print("This todo is not valid!")
				return False
			elif int(int(inputDue.group(i)) > int(match2.group(i))):
				break
		self.validDue = inputDue.group(0)
		return True

	def execute(self):
		descr = self.inputData[0]
		cat = self.inputData[2]
		sql = "insert into todo (what, due, category) values (?, ?, ?)"

		self.cur.execute(sql, (descr, self.validDue, cat,))
		self.conn.commit()
		print("\nYour plan has been successfully added!\n")


