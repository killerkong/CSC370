import sys, csv, psycopg2
from psycopg2 import sql

psql_user = 'ruizhang2018'
psql_db = 'sqlboys'
psql_password = 'V00926654'
psql_server = 'studentdb1.csc.uvic.ca'
psql_port = 5432
conn = psycopg2.connect(dbname=psql_db, user=psql_user,password=psql_password,host=psql_server, port=psql_port)

cur = conn.cursor()

def print_cur(cur):
    rows = cur.fetchall()
    for row in rows:
        print(row)
        
def get_table(table_name):
    sql = "select * from {};".format(table_name)
    cur.execute(sql)
    print_cur(cur)

def insert(table_name, values):
    cur.execute(SQL("insert into {} values%s;").format(Identifier(table_name)),values)
    
table_name = 'country'
values = ('default',"'Korea'")
insert(table_name, values)

get_table("country")

#conn.commit()
#cur.close()
#conn.close()
