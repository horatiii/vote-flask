import sqlite3

db = sqlite3.connect('../db/election_db')

cursor = db.cursor()

cursor.execute('select * from electors')

rows = cursor.fetchall()

print('electors')
for row in rows:
    print(row)

print()
cursor.execute('select * from candidates')
rows = cursor.fetchall()


print('candidates')
for row in rows:
    print(row) 
