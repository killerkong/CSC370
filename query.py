import psycopg2
psql_user = '###'
psql_db = 'sqlboys'
psql_password = '###'
psql_server = 'studentdb1.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname = psql_db, user = psql_user, password = psql_password, host = psql_server, port = psql_port)
cursor = conn.cursor()

sql = """
/* Drop tables if exist */
DROP TABLE IF EXISTS appointment CASCADE;
DROP TABLE IF EXISTS student_language CASCADE;
DROP TABLE IF EXISTS student CASCADE;
DROP TABLE IF EXISTS teacher_language CASCADE;
DROP TABLE IF EXISTS teacher CASCADE;
DROP TABLE IF EXISTS marked_worksheet CASCADE;
DROP TABLE IF EXISTS completed_worksheet CASCADE;
DROP TABLE IF EXISTS worksheet_language CASCADE;
DROP TABLE IF EXISTS worksheet CASCADE;
DROP TABLE IF EXISTS section CASCADE;
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS olympiads_group CASCADE;
DROP TABLE IF EXISTS country CASCADE;

/* Create tables */
CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL
);

CREATE TABLE olympiads_group (
    group_id SERIAL PRIMARY KEY,
    level INTEGER CHECK (level > 0 AND level < 13),
    entry_completion NUMERIC CHECK (entry_completion >= 0),
    entry_grade NUMERIC CHECK (entry_grade >= 0),
    country_id INTEGER REFERENCES country(id)
);

CREATE TABLE student (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    email VARCHAR(128) NOT NULL,
    credential VARCHAR(128) NOT NULL,
    skype_name VARCHAR(30),
    country_id INTEGER REFERENCES country(id),
    level INTEGER CHECK (level > 0 AND level < 13),
    average_mark NUMERIC CHECK (average_mark >= 0),
    completion NUMERIC CHECK (completion >= 0),
    olympiads_group_id INTEGER REFERENCES olympiads_group(group_id)
);

CREATE TABLE student_language (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES student(user_id),
    language VARCHAR(30) NOT NULL
);

CREATE TABLE teacher (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    email VARCHAR(128) NOT NULL,
    credential VARCHAR(128) NOT NULL,
    skype_name VARCHAR(30),
    country_id INTEGER REFERENCES country(id)
);

CREATE TABLE teacher_language (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES teacher(user_id),
    language VARCHAR(30) NOT NULL
);

CREATE TABLE appointment (
    appointment_id SERIAL PRIMARY KEY,
    teacher_id INTEGER REFERENCES teacher(user_id),
    student_id INTEGER REFERENCES student(user_id),
    day DATE NOT NULL,
    hour INTEGER CHECK (hour >= 0 AND hour < 24)
);

CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(30) NOT NULL
);

CREATE TABLE section (
    section_id SERIAL PRIMARY KEY,
    section_name VARCHAR(30) NOT NULL,
    category_id INTEGER REFERENCES category(category_id),
    previous_section_id INTEGER REFERENCES section(section_id),
    next_section_id INTEGER REFERENCES section(section_id)
);

CREATE TABLE worksheet (
    worksheet_id SERIAL PRIMARY KEY,
    level INTEGER CHECK (level > 0 AND level < 13),
    creator VARCHAR(30),
    category_id INTEGER REFERENCES category(category_id),
    section_id INTEGER REFERENCES section(section_id),
    path VARCHAR(128)
);

CREATE TABLE worksheet_language (
    id SERIAL PRIMARY KEY,
    worksheet_id INTEGER REFERENCES worksheet(worksheet_id),
    language VARCHAR(30) NOT NULL,
    book_link VARCHAR(128),
    math_concept TEXT
);

CREATE TABLE completed_worksheet (
    id SERIAL PRIMARY KEY,
    worksheet_id INTEGER REFERENCES worksheet(worksheet_id),
    user_id INTEGER REFERENCES student(user_id),
    upload_time TIMESTAMP NOT NULL,
    photo VARCHAR(128)
);

CREATE TABLE marked_worksheet (
    id SERIAL PRIMARY KEY,
    completed_worksheet_id INTEGER REFERENCES completed_worksheet(id),
    user_id INTEGER REFERENCES teacher(user_id),
    mark_time TIMESTAMP NOT NULL,
    mark NUMERIC CHECK (mark > 0),
    comment TEXT
);

/* Insert data */
INSERT INTO country(name) VALUES ('CANADA'), ('CHINA'), ('JAPAN');

INSERT INTO olympiads_group(level, entry_completion, entry_grade, country_id) VALUES
(1, 0.9, 90.0, 1),
(2, 0.9, 90.0, 1),
(3, 0.9, 90.0, 1),
(4, 0.9, 90.0, 1),
(5, 0.9, 90.0, 1),
(6, 0.9, 90.0, 1),
(7, 0.9, 90.0, 1),
(8, 0.9, 90.0, 1),
(9, 0.9, 90.0, 1),
(10, 0.9, 90.0, 1),
(11, 0.9, 90.0, 1),
(12, 0.9, 90.0, 1),
(1, 0.9, 90.0, 2),
(2, 0.9, 90.0, 2),
(3, 0.9, 90.0, 2),
(4, 0.9, 90.0, 2),
(5, 0.9, 90.0, 2),
(6, 0.9, 90.0, 2),
(7, 0.9, 90.0, 2),
(8, 0.9, 90.0, 2),
(9, 0.9, 90.0, 2),
(10, 0.9, 90.0, 2),
(11, 0.9, 90.0, 2),
(12, 0.9, 90.0, 2),
(1, 0.9, 90.0, 3),
(2, 0.9, 90.0, 3),
(3, 0.9, 90.0, 3),
(4, 0.9, 90.0, 3),
(5, 0.9, 90.0, 3),
(6, 0.9, 90.0, 3),
(7, 0.9, 90.0, 3),
(8, 0.9, 90.0, 3),
(9, 0.9, 90.0, 3),
(10, 0.9, 90.0, 3),
(11, 0.9, 90.0, 3),
(12, 0.9, 90.0, 3);

INSERT INTO category(category_name) VALUES
('Elementary Algebra'),
('Abstract Algebra'),
('Linear Algebra'),
('Algebraic Geometry'),
('Euclidean Geometry'),
('Differential Geometry'),
('Discrete Geometry'),
('Computational Geometry');

insert into section(section_name, category_id, previous_section_id, next_section_id) values ('head', null, null, null);
insert into section(section_name, category_id, previous_section_id, next_section_id) values('tail', null, null, null);
update section set next_section_id = (select section_id from section where section_name = 'tail') where section_name = 'head';
update section set previous_section_id = (select section_id from section where section_name = 'head') where section_name = 'tail';

insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Counting and number patterns', (select category_id from category where category_name = 'Elementary Algebra'), (select section_id from section where section_name = 'head'), (select section_id from section where section_name = 'tail'));

update section set next_section_id = (select section_id from section where section_name = 'Counting and number patterns') where section_name = 'head';
update section set previous_section_id = (select section_id from section where section_name = 'Counting and number patterns') where section_name = 'tail';

insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Addition', (select category_id from category where category_name = 'Elementary Algebra'), (select section_id from section where section_name = 'Counting and number patterns'), (select section_id from section where section_name = 'tail'));

update section set next_section_id = (select section_id from section where section_name = 'Addition') where section_name = 'Counting and number patterns';
update section set previous_section_id = (select section_id from section where section_name = 'Addition') where section_name = 'tail';

insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Subtraction', (select category_id from category where category_name = 'Elementary Algebra'), (select section_id from section where section_name = 'Addition'), (select section_id from section where section_name = 'tail'));

update section set next_section_id = (select section_id from section where section_name = 'Subtraction') where section_name = 'Addition';

update section set previous_section_id = (select section_id from section where section_name = 'Subtraction') where section_name = 'tail';

insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Comparing', (select category_id from category where category_name = 'Elementary Algebra'), (select section_id from section where section_name = 'Subtraction'), (select section_id from section where section_name = 'tail'));

update section set next_section_id = (select section_id from section where section_name = 'Comparing') where section_name = 'Subtraction';
update section set previous_section_id = (select section_id from section where section_name = 'Comparing') where section_name = 'tail';

insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Two-dimensional shapes', (select category_id from category where category_name = 'Algebraic Geometry'), (select section_id from section where section_name = 'Comparing'), (select section_id from section where section_name = 'tail'));

update section set next_section_id = (select section_id from section where section_name = 'Two-dimensional shapes') where section_name = 'Comparing';
update section set previous_section_id = (select section_id from section where section_name = 'Two-dimensional shapes') where section_name = 'tail';

insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Three-dimensional shapes', (select category_id from category where category_name = 'Algebraic Geometry'), (select section_id from section where section_name = 'Two-dimensional shapes'), (select section_id from section where section_name = 'tail'));

update section set next_section_id = (select section_id from section where section_name = 'Three-dimensional shapes') where section_name = 'Two-dimensional shapes';
update section set previous_section_id = (select section_id from section where section_name = 'Three-dimensional shapes') where section_name = 'tail';

insert into section (section_name, category_id, previous_section_id, next_section_id) values ('Patterns', (select category_id from category where category_name = 'Algebraic Geometry'), (select section_id from section where section_name = 'Three-dimensional shapes'), (select section_id from section where section_name = 'tail'));

update section set next_section_id = (select section_id from section where section_name = 'Patterns') where section_name = 'Three-dimensional shapes';
update section set previous_section_id = (select section_id from section where section_name = 'Patterns') where section_name = 'tail';

INSERT INTO 
    worksheet(level,creator,category_id,section_id,path)
VALUES
    (1,'John Doe',1,6,'https://drive.google.com/file/d/1SfIygCPM055jVme7rd3bZCGZaSBKslOZ'),
    (1,'Sam Smith',1,4,'https://drive.google.com/open?id=1buIYstl2OR-dkPbBbeixh5Zv68ShqnZY'),
    (1,'Steve Jobs',1,3,'https://drive.google.com/open?id=1mFLEML0l1BWMVywRE64DzS0x0LXA1fng');

INSERT INTO 
    worksheet_language(worksheet_id,language) 
VALUES
    (1,'SPANISH'),
    (2,'ENGLISH'),
    (3,'CHINESE');

INSERT INTO
    student(first_name,last_name,email,credential,skype_name,country_id,level,average_mark,completion,olympiads_group_id) 
VALUES
    ('William','Davis','williamdavis@yahoo.com','$2y$12$DVuJGXxpPhT.54lZ8g.T2.7E7qhX00U9a1.mVbEzJUGjbFURWEOA.','williamdavis',1,1,0.91,0.97,1),
    ('Oliver','Zhang','oliverzhang@yahoo.com','$2y$12$E7z726aIEiZJ/I3xFOoULuLawweR8dbPd7wnsndB2a7Ww7zxBcy4W','oliverzhang',1,7,0.0,0.0,NULL),
    ('Nobi','Nobita','nobinobita@yahoo.com','$2y$12$JwwbUu39VRYgdzD/uec5meSjxr8sSb43CBHh3JtJRnU1cEpul9n.q','nobinobita',1,3,0.0,0.0,NULL);

INSERT INTO 
    student_language(user_id,language) 
VALUES
    (1,'ENGLISH'),
    (2,'CHINESE'),
    (3,'JAPANESE'),
    (3,'SPANISH');

INSERT INTO 
    teacher(first_name,last_name,email,credential,skype_name,country_id)
VALUES
    ('Liam','Smith','liamsmith@uvic.ca','$2y$12$w9qYPk6Ffvajo.M0/xsnC.yzjoR9GBHYOTKAL6bKS9VebBf8egniG','liamsmith',1),
    ('Noah','Chen','noahchen@gmail.com','$2y$12$x9Q198RC.Mg21/6fdgrOC.4ubqf9hMPLAbBDo/OUL8E7K1CQxAis.','noahchen',2),
    ('Conan','Edogawa','conanedogawa@gmail.com','$2y$12$iIuUndBGG/RBqTuwg/afa.bl6kC4DWrRLZSBAL.nQkYfQjx0.khLS','conanedogawa',3);

INSERT INTO 
    teacher_language(user_id,language)
VALUES
    (1,'ENGLISH'),
    (1, 'SPANISH'),
    (2,'CHINESE'),
    (3,'JAPANESE');


INSERT INTO
    completed_worksheet(worksheet_id,user_id,upload_time,photo)
VALUES
    (1,3,'2019-11-15 10:00:00','https://drive.google.com/open?id=1HMLIVTJmK4L-AnwyyrGME2BP0qblZF0f'),
    (2,1,'2019-11-15 11:00:00','https://drive.google.com/open?id=1B-q9ClE_mYUIfa_6RLLjLxs-qpaNzzMN'),
    (3,2,'2019-11-15 10:00:00','https://drive.google.com/open?id=1Kcx1ZBdHfIDrh5Mr3RerEDbodm4cYa9y');

INSERT INTO
    marked_worksheet(completed_worksheet_id,user_id,mark_time,mark,comment) 
VALUES
    (1, 1, '2019-11-15 12:10:09', 100, '¡Excelente trabajo!'),
    (2, 1, '2019-11-15 12:30:10', 98, 'nice work!'),
    (3, 2, '2019-11-15 13:05:19', 100, '非常好!');

INSERT INTO 
    appointment(student_id, teacher_id, day, hour)
VALUES
    (1, 1, TO_DATE('21/12/2019', 'DD/MM/YYYY'), 13),
    (2, 2, TO_DATE('22/12/2019', 'DD/MM/YYYY'), 14),
    (3, 3, TO_DATE('22/12/2019', 'DD/MM/YYYY'), 14),
    (3, 3, TO_DATE('22/12/2019', 'DD/MM/YYYY'), 15);

"""

cursor.execute(sql)
conn.commit()
cursor.close()
conn.close()
