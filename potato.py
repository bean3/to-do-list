import sqlite3
import click
import re
import sys
import datetime

def create_db():

    global conn, cur

    conn = sqlite3.connect("potato.db")
    cur = conn.cursor()

    table_create_sql = """create table if not exists todo (
                id integer primary key autoincrement,
                what text not null,
                due text not null,
                category text not null,
                finished integer default 0);"""
    
    cur.execute(table_create_sql)

def exe_mk(mk):
    # due 가 정규식에 맞지 않으면 다시 입력 받는다.
    due = str(mk[1])
    regular = re.compile(r"(\d{4})[-](\d{2})[-](\d{2})[/](\d{2})[:](\d{2})")
    while True:
        if len(due) != 16:
            print("Please type in the right format : YYYY-MM-DD/HH:MM")
            sys.exit(1)
        match = regular.match(due)
        if match == None:
            print("Please type in the right format : YYYY-MM-DD/HH:MM")
            sys.exit(1)
        else:
            break

    s = datetime.datetime.now()
    regular2 = re.compile(r"(\d{4})[-](\d{2})[-](\d{2})\s(\d{2})[:](\d{2})")
    n = regular2.match(str(s))

    due = regular.match(mk[1])

    for i in range(1,6):
        if int(due.group(i)) < int(n.group(i)):
            print("This todo is not valid!")
            sys.exit(1)
        elif int(int(due.group(i)) > int(n.group(i))):
            break

    what = str(mk[0])

    sql = "insert into todo (what, due, category) values (?, ?, ?)"
    category = str(mk[2])
    cur.execute(sql, (what, due.group(0),category,))
    conn.commit()

def exe_rm(rm):

    sql = "delete from todo where id=?"
    task = (rm,)

    cur.execute(sql, task)
    conn.commit()

def exe_find(find):

    if(find == "%"):
        print("The corresponding result does not exist")
    else:
        sql = "SELECT * FROM todo WHERE what LIKE '%"+find+"%'"
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                for n in range(0,5):
                    if(n<4):
                        print(" | " + str(row[n]), end="")
                    else:
                        print(" | Done |" if row[3]==1 else " | In progress |", end="")
                print("")
        else:
            print("The corresponding result does not exist")



def exe_ctg(ct):#function that print only category that inserted. ex) work -> only print work categorylist
    
    sql = "select * from todo where category=?"
    cur.execute(sql,(ct,))
    rows = cur.fetchall()
    if rows:
        print(
                   "\n"
                "               P O T A T O F I E L D                                 \n"
                "=====================================================================\n"
                "| No.|   Description   |        Due       |    category     |  Status  |\n"
                "====================================================================="
                )

        for row in rows:

            #Get the columns
            num = row[0]
            wh = row[1]
            du = row[2]
            ctg = row[3]
            fin = row[4]
            if(ctg ==ct):

                print(
                    #Print the number of plan; Max : 2-digit number
                    "|", str(num).ljust(2),
                    #Print @#$^... if the description is too long to print; Max : 15 chars
                    "|", wh.ljust(15) if len(wh)<=15 else wh[:12] + "...",
                    #Print the due as it is since the due has its own format; YYYY-MM-DD

                    "|", du,
                    #print the category
                    "|", ctg.ljust(15) if len(wh)<=15 else wh[:12] + "...",
                    #Print whether the plan is done or not
                    "| Done        |" if fin==1 else "| In progress |"
                    )
            conn.commit()

        print(
                "======================================================================\n"
                #Dummy line, but planning to make pages
                "                                        Page 01/01 \n")
    else:
        print("The corresponding lists do not exist!")
        print("\nIf you forgot the category's name, type: python3 potato.py --cp ")

def ctg_print(cp):#카테고리 전체 보여주는 함수
    

    sql = "select * from todo where 1"
    cur.execute(sql)
    rows = cur.fetchall()
    print('================<category list>=============')
    for row in rows:

        #Get the columns
        num = row[0]
        wh = row[1]
        du = row[2]
        ctg = row[3]
        fin = row[4]
        

        print(
         
             ctg.ljust(15) 
           
            )
        conn.commit()

    print('===========================================')
    print('\nTo see only the values for a particular category, enter the following command')
    print('type:python3 potato.py --ct [category name]')


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
                du = str(input("Please type in the right format : YYYY-MM-DD/HH:MM"))
            match = regular.match(du)
            if match == None:
                du = str(input("Please type in the right format : YYYY-MM-DD/HH:MM"))
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
            "               P O T A T O F I E L D                                 \n"
            "=====================================================================\n"
            "| No.|   Description   |        Due      |   category     |  Status  |\n"
            "====================================================================="
            )

        for row in rows:

            #Get the columns
            num = row[0]
            wh = row[1]
            du = row[2]
            ctg = row[3]
            fin = row[4]

            print(
                #Print the number of plan; Max : 2-digit number
                "|", str(num).ljust(2),
                #Print @#$^... if the description is too long to print; Max : 15 chars
                "|", wh.ljust(15) if len(wh)<=15 else wh[:12] + "...",
                #Print the due as it is since the due has its own format; YYYY-MM-DD/HH:MM
                "|", du,
                #Print the category 
                "|", ctg.ljust(15) if len(wh)<=15 else wh[:10] + "...",
                #Print whether the plan is done or not
                "| Done        |" if fin==1 else "| In progress |"
                )

        print(
            "=====================================================================\n"
            #Dummy line, but planning to make pages
            "                                              Page 01/01 \n")

    else:
        print("Nothing to print :(\n")

@click.command()
#Basic options
@click.option('--mk', nargs=3, type=str, help='Make a new plan: [descr.] [due] [category]')
@click.option('--rm', type=int, help='Remove your plan: [number]')
@click.option('--mod', help='Modify your plan: [number]')
@click.option('--find', type=str, help='find your plan: [text]')
@click.option('--ct', type=str, help='print only category that you inserted')
@click.option('--cp',  'cp',flag_value='cp',help='print all your category that have')
#Printing options
@click.option('--uf', 'p_opt', flag_value='unfinished', help='Print your unfinished plans')
@click.option('--f', 'p_opt', flag_value='finished', help='Print your finished plans')
def run(mk, rm, mod, cp, ct, p_opt, find):

    create_db()
    print_option = None

    #Check the option
    if mk:
        exe_mk(mk)
    elif rm:
        exe_rm(rm)
    elif mod:
        exe_mod(mod)
    elif cp:
        ctg_print(cp)
        return
    elif ct:
        exe_ctg(ct)
        return
    elif find:
    	exe_find(find)
    	return
    elif p_opt:
        print_option = p_opt

    cur.execute("select * from todo where 1")
    rows = cur.fetchall()

    # if rows:
    #     for row in rows:
    #         iregular = re.compile(r"(\d{4})[-](\d{2})[-](\d{2})\s(\d{2})[:](\d{2})")
    #         iregular2 = re.compile(r"(\d{4})[-](\d{2})[-](\d{2})\s(\d{2})[:](\d{2})")

    #         idue = row[2]
    #         i_match = iregular.match(idue)

    #         t = datetime.datetime.now()
    #         now = iregular2.match(str(t))

    #         for i in range(1,6):
    #             if int(i_match.group(i)) < int(now.group(i)):
    #                 sql = "delete from todo where due = ?"

    #                 cur.execute(sql, (i_match.group(0)))
    #                 conn.commit()
    #             elif int(i_match.group(i)) > int(now.group(i)):
    #                 break

    print_list(print_option)
    conn.close()

if __name__ == '__main__':
    run()
