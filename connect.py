import sys, csv, psycopg2

psql_user = 'ruizhang2018'
psql_db = 'sqlboys'
psql_password = 'V00926654'
psql_server = 'studentdb1.csc.uvic.ca'
psql_port = 5432
conn = psycopg2.connect(dbname=psql_db, user=psql_user,password=psql_password,host=psql_server, port=psql_port)

cur = conn.cursor()



def get_table(table_name):
    cur.execute(SQL("select * from %s;").format(Identifier(table_name),))

country = 'country'
get_table(country)

conn.commit()
cur.close()
conn.close()
