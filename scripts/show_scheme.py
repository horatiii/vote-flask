"""
shows general db scheme
"""
import sqlite3

DB = sqlite3.connect('../db/election_db')

CURSOR = DB.cursor()

CURSOR.execute('select * from electors')

ROWS = CURSOR.fetchall()

print('electors')
for row in ROWS:
    print(row)

print()
CURSOR.execute('select * from candidates')
ROWS = CURSOR.fetchall()


print('candidates')
for row in ROWS:
    print(row)

DB.close()
