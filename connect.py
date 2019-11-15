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

def insert_category():
    cur.execute("insert into category(category_name) values ('Elementary Algebra');")
    cur.execute("insert into category(category_name) values ('Abstract Algebra');")
    cur.execute("insert into category(category_name) values ('Linear Algebra');")
    cur.execute("insert into category(category_name) values ('Algebraic Geometry');")
    cur.execute("insert into category(category_name) values ('Euclidean Geometry');")
    cur.execute("insert into category(category_name) values ('Differential Geometry');")
    cur.execute("insert into category(category_name) values ('Discrete Geometry');")
    cur.execute("insert into category(category_name) values ('Computational Geometry');")

def insert_section():
    cur.execute("insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Functions', select category_id from category where category_name = 'Elementary Algebra', 1, 1);")
    cur.execute("insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Transformators', select category_id from category where category_name = 'Elementary Algebra', 1, 3);")
    cur.execute("insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Polynomial Functions', select category_id from category where category_name = 'Elementary Algebra', 2, 4);")
    cur.execute("insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Exponential Functions', select category_id from category where category_name = 'Elementary Algebra', 3, 5);")
    cur.execute("insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Trigonometry', select category_id from category where category_name = 'Algebraic Geometry', 4, 6);")
    cur.execute("insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Two-dimensional Vectors', select category_id from category where category_name = 'Linear Algebra', 5, 7);")
    cur.execute("insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Three-dimensional Vectors', select category_id from category where category_name = 'Linear Algebra', 6, 18;")
    
#insert_category()
insert_section()
get_table("category")
get_table("section")

conn.commit()
cur.close()
conn.close()
