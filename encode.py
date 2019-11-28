

def insert(table_name, values):
    sql = "insert into {} values {}".format(table_name, values)
    print(sql)
    
def insert_section(section_name, category_name, previous_section, next_section):
    sql = "insert into section (section_name, category_id, previous_section_id, next_section_id) values ('{}', (select category_id from category where category_name = '{}'), (select section_id from section where section_name = '{}'), (select section_id from section where section_name = '{}'));".format(section_name, category_name, previous_section, next_section)
    
    sql_previous = "update section set next_section_id = (select section_id from section where section_name = '{}') where section_name = '{}';".format(section_name, previous_section)
    
    sql_next = "update section set previous_section_id = (select section_id from section where section_name = '{}') where section_name = '{}';".format(section_name, next_section)
    
    print(sql)
    print(sql_previous)
    print(sql_next)
    
insert_section('Functions', 'Algebra', 'Function Concept', 'Radical Functions')
