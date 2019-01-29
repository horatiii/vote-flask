import sqlite3
import uuid

db = sqlite3.connect('../db/election_db')
cursor = db.cursor()

#candidates
cursor.execute('''  
        drop table if exists candidates
        ''') 
cursor.execute('''create table candidates(name text primary key)''')
print('loading candidates:')

with open('../data/candidates') as fp:
    for i in fp.readlines():
        cursor.execute('''insert into candidates values(?)''',(str(i).strip('\n'),))

db.commit()

cursor.execute('''select * from candidates''')
all_rows = cursor.fetchall()
for row in all_rows:
    print(row)
#create table
cursor.execute('''  
        drop table if exists electors
        ''') 
cursor.execute('''
        create table if not exists electors(id integer primary key, secret_key text, vote text, date_of_vote text,
        foreign key(vote) references candidates(name))
        ''')

with open('../data/electors') as fp:
    for i in fp.readlines():

        cursor.execute('''
                insert or replace into electors(id, secret_key) values(?,?)
                ''',(i,str(uuid.uuid4())[:8]))
db.commit()



print('electors loaded:')

cursor.execute('select * from electors')

all_rows = cursor.fetchall()

for row in all_rows:
    print(row)



db.close()

