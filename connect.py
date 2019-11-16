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

    
def insert_section(section_name, category_name, previous_section, next_section):
    sql = "insert into section (section_name, category_id, previous_section_id, next_section_id) values ('{}', (select category_id from category where category_name = '{}'), (select section_id from section where section_name = '{}'), (select section_id from section where section_name = '{}'));".format(section_name, category_name, previous_section, next_section)
    
    sql_previous = "update section set next_section_id = (select section_id from section where section_name = '{}') where section_name = '{}';".format(section_name, previous_section)
    
    sql_next = "update section set previous_section_id = (select section_id from section where section_name = '{}') where section_name = '{}';".format(section_name, next_section)
    
    cur.execute(sql)
    cur.execute(sql_previous)
    cur.execute(sql_next)
    #print(sql)
    #print(sql_previous)
    #print(sql_next)
    
    
#insert_category()
cur.execute("insert into section(section_name, category_id, previous_section_id, next_section_id) values ('head', null, null, null)")
cur.execute("insert into section(section_name, category_id, previous_section_id, next_section_id) values('tail', null, null, null)")
cur.execute("update section set next_section_id = (select section_id from section where section_name = 'tail') where section_name = 'head';")
cur.execute("update section set previous_section_id = (select section_id from section where section_name = 'head') where section_name = 'tail';")

insert_section('Functions', 'Elementary Algebra', 'head', 'tail')
insert_section('Transformators', 'Elementary Algebra', 'Functions', 'tail')
insert_section('Polynomial Functions', 'Elementary Algebra', 'Transformators', 'tail')
insert_section('Exponential Functions', 'Elementary Algebra', 'Polynomial Functions', 'tail')
insert_section('Trigonometry', 'Algebraic Geometry', 'Exponential Functions', 'tail')
insert_section('Two-dimensional Vectors', 'Linear Algebra', 'Trigonometry', 'tail')
insert_section('Three-dimensional Vectors', 'Linear Algebra', 'Two-dimensional Vectors', 'tail')
get_table("category")
get_table("section")

#conn.commit()
#cur.close()
#conn.close()
