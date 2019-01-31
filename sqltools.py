"""
Auxiliary functions for db operations
"""

import sqlite3
DB_PATH = 'db/election_db'


def get_bar_values():
    """
    returns data for representing voting results
    """
    db_ = sqlite3.connect(DB_PATH)
    cursor = db_.cursor()
    cursor.execute('''select candidates.name, count(electors.vote) \
                   from candidates left outer join electors on \
                   electors.vote = candidates.name group by candidates.name;''')
    fetched = cursor.fetchall()
    labels = [i[0] for i in fetched]
    values = [i[1] for i in fetched]
    db_.close()
    return labels, values


def fetch(command, args=''):
    """
    command is obligatory,
    args are optional.
    i.e fetch(select * from candidates where name=?, ('A',))
    returns result from sqlite database.
    """
    db_ = sqlite3.connect(DB_PATH)
    cursor = db_.cursor()
    cursor.execute(command, args)
    data = cursor.fetchall()
    db_.close()
    return data


def update(command, args):
    """
    enables to insert data to the db.
    i.e update('insert into candidates(name) values(?)', ('D',))


    returns nothing
    """
    db_ = sqlite3.connect(DB_PATH)
    cursor = db_.cursor()
    cursor.execute(command, args)
    db_.commit()
    db_.close()


def make_vote(candidate, elector):
    """
    responsible for updating table electors with given candidate and elector
    returns result of operation
    """
    db_ = sqlite3.connect(DB_PATH)
    cursor = db_.cursor()
    cursor.execute('update electors set vote = ? where id = ?', (candidate, elector))
    db_.commit()
    cursor.execute('select count() from electors where vote = ? and id = ?', (candidate, elector))
    success = cursor.fetchall()[0][0] == 1
    print('vote succeed: ', success)
    db_.close()
    return success


def get_candidates():
    """
    returns candidates for home view
    """
    db_ = sqlite3.connect(DB_PATH)
    cursor = db_.cursor()
    cursor.execute('select name from candidates')
    rows = cursor.fetchall()
    rows = [i[0] for i in rows]
    db_.close()
    return rows

def credentials_valid(elector_id, secret_key):
    """
    checks whether credentials provided by the user are valid
    """
    db_ = sqlite3.connect(DB_PATH)
    cursor = db_.cursor()
    cursor.execute('select exists(select id from electors where id = ? and secret_key = ?)', \
                   (elector_id, secret_key))
    return cursor.fetchall()[0][0] == 1

def can_vote(elector_id, secret_key):
    """
    checks whether given elector has not voted before
    """
    db_ = sqlite3.connect(DB_PATH)
    cursor = db_.cursor()
    cursor.execute('select NULL is (select vote from electors where id = ? and secret_key = ?)', \
                   (elector_id, secret_key))
    return cursor.fetchall()[0][0] == 1

def candidate_valid(option):
    """
    checks whether given candidate exists in database
    """
    db_ = sqlite3.connect(DB_PATH)
    cursor = db_.cursor()
    cursor.execute('select exists(select name from candidates where name = ?)', (option,))
    return cursor.fetchall()[0][0] == 1
