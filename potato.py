import sqlite3
import click
import re

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
    # due 가 정규식에 맞지 않으면 다시 입력 받는다.
    due = str(mk[1])
    regular = re.compile(r"(\d{4})[-](\d{2})[-](\d{2})[/](\d{2})[:](\d{2})")
    while True:
        if len(due) != 16:
            print("Please type in the right format : YYYY-MM-DD HH:MM")
            sys.exit(1)
        match = regular.match(due)
        if match == None:
            print("Please type in the right format : YYYY-MM-DD HH:MM")
            sys.exit(1)
        else:
            break
    due = regular.match(mk[1])

    what = str(mk[0])

    sql = "insert into todo (what, due) values (?, ?)"

    cur.execute(sql, (what, due.group(0),))
    conn.commit()

def exe_rm(rm):

    sql = "delete from todo where id=?"
    task = (rm,)

    cur.execute(sql, task)
    conn.commit()

def exe_mod(mod):

    cur.execute("select * from todo where 1")
    rows = cur.fetchall()
    cur.execute("select * from todo where id=?", (mod,))
    row = cur.fetchall()

    if mod.isdigit() and row and int(mod)<=len(rows) and mod > '0':
        print("\n(Nothing will change if you enter nothing.)")

        wh = str(input("What's your new plan?: "))
        wh = wh if wh else row[0][1] # Check if inputs are empty; nothing will change if input is empty
        
        du = str(input("When is the due date? : "))
        du = du if du else row[0][2] # Check if inputs are empty; nothing will change if input is empty
        regular = re.compile(r"(\d{4})[-](\d{2})[-](\d{2})[/](\d{2})[:](\d{2})")
        while True:
            while len(du) != 16:
                du = str(input("When is the due date? : "))
            match = regular.match(du)
            if match == None:
                du = str(input("When is the due date? : "))
            else:
                break
        

        
        fin = str(input("Is it finished?(Y/N) : "))
        while(fin != 'Y' and fin != 'N' and fin !=''):
            fin = str(input('Is it finished?(Y/N) : '))
        if fin == "Y":
            fin = 1
        elif fin == "N":
            fin = 0
        else:
            fin = fin if fin else row[0][3] # Check if inputs are empty; nothing will change if input is empty
        

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

    if rows:

        print(
            "\n"
            "                   P O T A T O F I E L D                 \n"
            "=========================================================\n"
            "| No.|   Description   |       Due        |   Status    |\n"
            "========================================================="
            )

        for row in rows:

            #Get the columns
            num = row[0]
            wh = row[1]
            du = row[2]
            fin = row[3]

            print(
                #Print the number of plan; Max : 2-digit number
                "|", str(num).ljust(2),
                #Print @#$^... if the description is too long to print; Max : 15 chars
                "|", wh.ljust(15) if len(wh)<=15 else wh[:12] + "...",
                #Print the due as it is since the due has its own format; YYYY-MM-DD
                "|", du,
                #Print whether the plan is done or not
                "| Done        |" if fin==1 else "| In progress |"
                )

        print(
            "=========================================================\n"
            #Dummy line, but planning to make pages
            "                                              Page 01/01 \n")

    else:
        print("Nothing to print :(\n")

@click.command()
#Basic options
@click.option('--mk', nargs=2, type=str, help='Make a new plan: [descr.] [due]')
@click.option('--rm', type=int, help='Remove your plan: [number]')
@click.option('--mod', help='Modify your plan: [number]')
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
