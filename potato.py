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
                category text,
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
        print("No matches found")

    else:
        cur.execute("select * from todo where what like '%" + find + "%'")
        rows = cur.fetchall()

        if rows:
            while True:
                print_find_result(rows)

                num = input("Enter the number of plan you want to see details (0 : Exit) : ")
                while num.isdigit() != True:
                    num = input("Enter the number of plan you want to see details (0 : Exit) : ")

                if num == '0':
                     break
                else:
                     print_detail(num)
                     input("Press Enter to continue...")

        else:
            print("No matches found")

def print_find_result(rows):

    print(
        "\n",
        len(rows), " matches found\n"
        "\n"
        "No. | Description\n"
        "===================================================", sep = ""
        )

    for row in rows:

        #You can see only 2 informations before using plan_detail function
        num = row[0]
        wh = row[1]

        print(
            str(num).ljust(3) + " | ",
            wh if len(wh) <= 45 else wh[:42] + "...", sep = ""
            )

    print("===================================================")

def print_detail(num):

    cur.execute("select * from todo where id=?", (num,))
    row = cur.fetchall()

    if row:
        row = row[0]

        #Get the columns
        num = row[0]
        wh = row[1]
        du = row[2]
        cat = row[3]
        fin = row[4]

        print(
            "\nNo. ", num,
            "\nDescription : ", wh,
            "\nDue : ", du,
            "\nCategory : ", cat,
            "\nStatus : ", "Done\n" if fin == 1 else "In progress\n", sep = "")

    else:
        print("\nInvaild number :(\n")

def get_cats():

    sql = "select category from todo where 1"
    cur.execute(sql)
    existing_cats = cur.fetchall()

    #return ['cat1', 'cat2', ...]
    return {cat[0] for cat in existing_cats}

def check_cat():

    print_cat_list()

    existing_cats = get_cats()
    selected_cat = input("What category do you want to see? : ")

    if selected_cat in existing_cats:
        return selected_cat

    else:
        print("There is no category named "+ selected_cat + "!")
        return "null"

def print_cat_list():

    existing_cats = get_cats()

    print()
    for cat in existing_cats:
        print("[" + cat + "]", end=" ")
    print("\n")

def exe_mod(mod):

    cur.execute("select * from todo where 1")
    rows = cur.fetchall()
    cur.execute("select * from todo where id=?", (mod,))
    row = cur.fetchall()

    if mod.isdigit() and row and int(mod) <= len(rows) and mod > '0':
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
    'finished': "select * from todo where finished=1",
    'category': "select * from todo where category='" + check_cat() + "'" if p_opt == 'category' else None

    }.get(p_opt, default)

def print_list(pg, p_opt):

    cur.execute(check_print_option(p_opt))
    rows = cur.fetchall()

    #Page settings
    rowsinPage = 10
    rowsinLastPage = len(rows) % rowsinPage
    calcPageNum = len(rows) // rowsinPage #To calculate maximum page number
    maxPageNum = calcPageNum if rowsinLastPage == 0 else calcPageNum + 1

    if rows:

        #Print if the pg is existing page number, else terminate
        if pg not in range(0, maxPageNum + 1):
            print("\nNo pages found\n")
            return

        print(
            "\n"
            "                         P O T A T O F I E L D                         "
            )

        for page in range(0, maxPageNum):

            #Check whether the pg option was given and pg is same with page number
            if (pg != 0 and page+1 != pg):
                continue

            print(
                "=======================================================================\n"
                "| No. |   Description   |       Due        |  Category  |   Status    |\n"
                "======================================================================="
                )

            rowIndex = page * rowsinPage

            for row in rows[rowIndex:rowIndex + rowsinPage]:

                #Get the columns
                num = row[0]
                wh = row[1]
                du = row[2]
                cat = row[3]
                fin = row[4]

                print(
                    #Print the number of plan; Max : 2-digit number
                    "|", str(num).ljust(3),
                    #Print @#$^... if the description is too long to print; Max : 15 chars
                    "|", wh.ljust(15) if len(wh)<=15 else wh[:12] + "...",
                    #Print the due as it is since the due has its own format; YYYY-MM-DD
                    "|", du,
                    #Print the category in the similar way to the description
                    "|", cat.ljust(10) if len(cat)<=10 else cat[:7] + "...",
                    #Print whether the plan is done or not
                    "| Done        |" if fin==1 else "| In progress |"
                    )

            print(
                "=======================================================================\n"
                "                                                            Page "
                "0" + str(page + 1) if len(str(page)) == 1 else page, "/"
                "0" + str(maxPageNum) if len(str(maxPageNum)) == 1 else maxPageNum,
                "\n", sep = "")

    else:
        print("\nNothing to print :(\n")

@click.command()
#Basic options
@click.option('--mk', nargs=3, type=str, help='Make a new plan: [descr.] [due] [category]')
@click.option('--rm', type=int, help='Remove your plan: [number]')
@click.option('--mod', help='Modify your plan: [number]')
@click.option('--find', type=str, help='Find your plan: [text]')
@click.option('--det', type=int, help='Show details of plan: [number]')
#Printing options
@click.option('--pg', type=int, default=0, help='Print the page of which you enter: [page]')
@click.option('--cat', 'p_opt', flag_value='category', help='Print the plans for category which you will select')
@click.option('--uf', 'p_opt', flag_value='unfinished', help='Print your unfinished plans')
@click.option('--f', 'p_opt', flag_value='finished', help='Print your finished plans')
def run(mk, rm, mod, find, det, pg, p_opt):

    create_db()
    print_option = None

    #Check the option
    if mk:
        exe_mk(mk)
    elif rm:
        exe_rm(rm)
    elif mod:
        exe_mod(mod)
    elif find:
        exe_find(find)
        conn.close()
        return
    elif det:
        print_detail(det)
        conn.close()
        return
    elif p_opt:
        print_option = p_opt

    # cur.execute("select * from todo where 1")
    # rows = cur.fetchall()

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

    print_list(pg, print_option)
    conn.close()

if __name__ == '__main__':
    run()
