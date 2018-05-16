import sqlite3
import click

def create_db():

    global conn, cur

    conn = sqlite3.connect("potato.db")
    cur = conn.cursor()

    table_create_sql = """create table if not exists todo (
                id integer primary key autoincrement,
                what text not null,
                due text not null,
                finished integer default 0);"""
    
    cur.execute(table_create_sql)

def exe_mk(mk):

    sql = "insert into todo (what, due) values (?, ?)"
    task = mk

    cur.execute(sql, task)
    conn.commit()

def exe_rm(rm):

    sql = "delete from todo where id=?"
    task = (rm,)

    cur.execute(sql, task)
    conn.commit()

def exe_mod(mod):

    cur.execute("select * from todo where id=?", (mod,))
    row = cur.fetchall()

    if row:
        print("\n(Nothing will change if you enter nothing.)")
        wh = str(input("What's your new plan?: "))
        du = str(input("When is the due date? : "))
        fin = str(input("Is it finished?(Y/N) : "))
        while(fin != 'Y' and fin != 'N'):
            fin = str(input('Is it finished?(Y/N) : '))
        fin = 1 if fin == "Y" else 0

        #Check if inputs are empty; nothing will change if input is empty
        wh = wh if wh else row[0][1]
        du = du if du else row[0][2]

        sql = "update todo set what=?, due=?, finished=? where id=?"
        task = (wh, du, fin, mod)

        cur.execute(sql, task)
        conn.commit()

    else:
    	print("\nInvalid number; check it again! :(")

def check_print_option(p_opt):

    default = "select * from todo where 1"

    return{

    'unfinished': "select * from todo where finished=0",
    'finished': "select * from todo where finished=1"

    }.get(p_opt, default)

def print_list(p_opt):

    cur.execute(check_print_option(p_opt))
    rows = cur.fetchall()

    print("")
    if rows:
        for row in rows:
            for n in range(0,4):
                if(n<3):
                    print(" | " + str(row[n]), end="")
                else:
                    print(" | Done |" if row[3]==1 else " | In progress |", end="")
            print("")
    else:
        print("Nothing to print :(")

@click.command()
#Basic options
@click.option('--mk', nargs=2, type=str, help='Make a new plan: [descr.] [due]')
@click.option('--rm', type=int, help='Remove your plan: [number]')
@click.option('--mod', type=int, help='Modify your plan: [number]')
#Printing options
@click.option('--uf', 'p_opt', flag_value='unfinished', help='Print your unfinished plans')
@click.option('--f', 'p_opt', flag_value='finished', help='Print your finished plans')
def run(mk, rm, mod, p_opt):

    create_db()
    print_option = None

    #Check the option
    if mk:
        exe_mk(mk)
    elif rm:
        exe_rm(rm)
    elif mod:
        exe_mod(mod)
    elif p_opt:
        print_option = p_opt

    print_list(print_option)
    conn.close()

if __name__ == '__main__':
    run()