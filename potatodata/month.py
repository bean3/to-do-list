from detail import Detail

class Month():
   def __init__(self, db, key):
      self.cur = db.cur
      self.conn = db.conn
      self.monthKey = key
      self.detail = Detail(db, None)

   def check(self):
      sql = "SELECT * FROM todo WHERE due LIKE strftime('%Y','now')||'-"+format(self.monthKey, '02')+"'||'%'"
      self.cur.execute(sql)
      self.resultRows = self.cur.fetchall()

      for row in self.resultRows:
         num = row[0]
         descr = row[1] if len(row[1]) <= 45 else row[1][:42] + "..."

      if self.resultRows:
         return True
      else:
         print("have nothing to do this month. Make something to do~")
         return False

   def execute(self):

      while True:
         print(
            "\n",
            #len(self.resultRows), " matches found\n"
            " Have " ,len(self.resultRows) ," thing to do this month.\n"
            "\n"
 			"=======================================================================\n"
			"| No. |   Description   |       Due        |  Category  |   Status    |\n"
			"=======================================================================", sep = "")

         for row in self.resultRows:
            num = row[0]
            descr = row[1] if len(row[1]) <= 45 else row[1][:42] + "..."
            due = row[2]
            cat = row[3] if len(row[3]) <= 10 else row[3][:7] + "..."
            fin = "Done" if row[4] == 1 else "In Progress"

            print(f"| {num:3} | {descr:15} | {due} | {cat:10} | {fin:11} |")

         print("=======================================================================")

         while True:
            if self.detail.check():
               self.detail.execute()
               input("Press Enter to continue...")
               self.detail.planNum = None
               break

            self.detail.planNum = None