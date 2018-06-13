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

global db
db = DB()

@click.group()
@click.pass_context
def run(ctx):
	"""Thank you for using Potatofield!\n
	To get more information, please visit our wiki:\n
	https://github.com/bean3/to-do-list/wiki"""

#Commands

@run.command()
@click.option('--what', type=str, metavar='<TEXT>', help='What is your plan?')
@click.option('--due', type=str, metavar='<YYYY-MM-DD/HH-MM>', help='When is the due date?')
@click.option('--cat', type=str, metavar='<TEXT>', help='Categorize your plan!')
def make(what, due, cat):
	"""Make a new plan."""
	cmd = Make(db, [what, due, cat])
	need = []
	need += ['what'] if not what else []
	need += ['due'] if not due else []
	need += ['cat'] if not cat else []
	cmd.interactive()
	if cmd.check():
		cmd.execute()

@run.command()
@click.argument('num', type=click.IntRange(1,), default=1)
@click.option('--all', is_flag=True)
def remove(num, all):
	"""Remove the plan which you will select."""
	cmd = Remove(db, num, all)
	if cmd.check():
		cmd.execute()

@run.command()
@click.argument('num', type=click.IntRange(1,))
@click.option('--what', type=str, metavar='<TEXT>', help='Change the description.')
@click.option('--due', type=str, metavar='<YYYY-MM-DD/HH-MM>', help='Change the due date.')
@click.option('--cat', type=str, metavar='<TEXT>', help='Change the category.')
@click.option('--fin', type=click.IntRange(0,1), metavar='<0:NO/1:YES>', help='Change the status.')
def modify(num, what, due, cat, fin):
	"""Modify the plan which you will select."""
	cmd = Modify(db, num, [what, due, cat, fin])
	if cmd.isExist():
		cmd.interactive()
		if 'due' not in cmd.need:
			if cmd.check():
				cmd.execute()
		else:
			cmd.execute()
	else:
		print("\nInvalid number :(\n")

@run.command()
@click.option('--what', type=str, metavar='<TEXT>', help='Search the plans which contain the keyword in description.')
@click.option('--month', type=click.IntRange(1,12), metavar='<NUM>', help='Search the plans of the month you entered.')
def find(what, month):
	"""Search the plan containing the input keyword."""
	cmd = Find(db, what, month)
	if cmd.check():
		cmd.execute()

@run.command()
@click.argument('num', type=click.IntRange(1,))
def detail(num):
	"""Show the details of selected plan."""
	cmd = Detail(db, num)
	if cmd.check():
		cmd.execute()

@run.command()
@click.option('--pg', type=click.IntRange(1,), help='Print the page of which you enter.', metavar='<NUM>')
@click.option('--cat', 'p_opt', flag_value='category', help='Select the category and print the plans for it.')
@click.option('--uf', 'p_opt', flag_value='unfinished', help='Print your unfinished plans.')
@click.option('--f', 'p_opt', flag_value='finished', help='Print your finished plans.')
@click.option('--od', 'p_opt', flag_value='overdue', help='Print your overdue plans.')
def show(pg, p_opt):
	"""Print out the plans.\n
	You can see the all plans if there is no options."""
	db.renew()
	Plan(db, pg, p_opt).show()

@run.command()
def version():
	"""Show the current version."""
	cmd = Version()
	cmd.execute()

if __name__ == '__main__':
	run()