import sqlite3
import click

from .db import DB
from .make import Make
from .remove import Remove
from .modify import Modify
from .find import Find
from .detail import Detail
from .plan import Plan
from .version import Version

@click.command()

#Basic options
@click.option('--mk', nargs=3, type=str, help='Make a new plan.', metavar='[descr.] [due] [cat.]')
@click.option('--rm', type=click.IntRange(1,), help='Remove your plan.', metavar='[num.]')
@click.option('--mod', help='Modify your plan.', metavar='[num.]')
@click.option('--find', type=str, help='Find your plan.', metavar='[str.]')
@click.option('--det', type=click.IntRange(1,), help='Show details of selected plan.', metavar='[num.]')

#Printing options
@click.option('--pg', type=click.IntRange(0,), default=0, help='Print the page of which you enter.', metavar='[num.]')
@click.option('--cat', 'p_opt', flag_value='category', help='Select the category and print the plans for it.')
@click.option('--uf', 'p_opt', flag_value='unfinished', help='Print your unfinished plans.')
@click.option('--f', 'p_opt', flag_value='finished', help='Print your finished plans.')
@click.option('--od', 'p_opt', flag_value='overdue', help='Print your overdue plans.')
@click.option('--ver', is_flag = True, help='Print the current version.')


def run(mk, rm, mod, find, det, ver, pg, p_opt):
	"""Thank you for using Potatofield!\n
	To get more information, please visit our wiki:\n
	https://github.com/bean3/to-do-list/wiki"""
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
	elif ver:
		cliOption = Version()
	elif p_opt:
		printOption = p_opt

	if cliOption != None:
		if cliOption.check():
			cliOption.execute()
		db.conn.close()
		return

	DB().renew()
		
	Plan(db, pg, printOption).show()
	db.conn.close()

if __name__ == '__main__':
	run()




