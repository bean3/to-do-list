import sqlite3
import click
import sys

sys.path.insert(0, './data')
from db import DB
from make import Make
from remove import Remove
from modify import Modify
from find import Find
from detail import Detail
from plan import Plan

@click.command()

#Basic options
@click.option('--mk', nargs=3, type=str, help='Make a new plan: [descr.] [due] [category]')
@click.option('--rm', type=click.IntRange(1,), help='Remove your plan: [number]')
@click.option('--mod', help='Modify your plan: [number]')
@click.option('--find', type=str, help='Find your plan: [text]')
@click.option('--det', type=click.IntRange(1,), help='Show details of plan: [number]')

#Printing options
@click.option('--pg', type=click.IntRange(0,), default=0, help='Print the page of which you enter: [page]')
@click.option('--cat', 'p_opt', flag_value='category', help='Print the plans for category which you will select')
@click.option('--uf', 'p_opt', flag_value='unfinished', help='Print your unfinished plans')
@click.option('--f', 'p_opt', flag_value='finished', help='Print your finished plans')

def run(mk, rm, mod, find, det, pg, p_opt):
	db = DB()
	cliOption = None
	printOption = None

	#Check which option is given
	if mk:
		cliOption = Make(db, mk)
	elif rm:
		cliOption = Remove(db, rm)
	elif mod:
		cliOption = Modify(db, mod)
	elif find:
		cliOption = Find(db, find)
	elif det:
		cliOption = Detail(db, det)
	elif p_opt:
		printOption = p_opt

	#Dummy lines

	# cur.execute("select * from todo where 1")
	# rows = cur.fetchall()

	# if rows:
	# 	for row in rows:
	# 		iregular = re.compile(r"(\d{4})[-](\d{2})[-](\d{2})\s(\d{2})[:](\d{2})")
	# 		iregular2 = re.compile(r"(\d{4})[-](\d{2})[-](\d{2})\s(\d{2})[:](\d{2})")

	# 		idue = row[2]
	# 		i_match = iregular.match(idue)

	# 		t = datetime.datetime.now()
	# 		now = iregular2.match(str(t))

	# 		for i in range(1,6):
	# 			if int(i_match.group(i)) < int(now.group(i)):
	# 				sql = "delete from todo where due = ?"

	# 				cur.execute(sql, (i_match.group(0)))
	# 				conn.commit()
	# 			elif int(i_match.group(i)) > int(now.group(i)):
	# 				break

	if cliOption != None:
		if cliOption.check():
			cliOption.execute()
		db.conn.close()
		return

	Plan(db, pg, printOption).show()
	db.conn.close()

if __name__ == '__main__':
	run()




