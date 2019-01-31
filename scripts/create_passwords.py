"""
for db relation and data generation
"""
import sqlite3
import uuid

DB = sqlite3.connect('../db/election_db')
CURSOR = DB.cursor()

#candidates
CURSOR.execute('''
        drop table if exists candidates
        ''')
CURSOR.execute('''create table candidates(name text primary key)''')
print('loading candidates:')

with open('../data/candidates') as fp:
    for i in fp.readlines():
        CURSOR.execute('''insert into candidates values(?)''', (str(i).strip('\n'),))

DB.commit()

CURSOR.execute('''select * from candidates''')
ROWS = CURSOR.fetchall()
for row in ROWS:
    print(row)
#create table
CURSOR.execute('''
        drop table if exists electors
        ''')
CURSOR.execute('''
        create table if not exists electors(id integer primary key, secret_key text, vote text, date_of_vote text,
        foreign key(vote) references candidates(name))
        ''')

with open('../data/electors') as fp:
    for i in fp.readlines():
        CURSOR.execute(''' insert or replace into electors(id, secret_key) values(?,?) ''', \
                       (i, str(uuid.uuid4())[:8]))

DB.commit()



print('electors loaded:')

CURSOR.execute('select * from electors')

ROWS = CURSOR.fetchall()

for row in ROWS:
    print(row)

DB.close()
