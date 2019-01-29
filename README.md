Voting system built in python3 with use of sqlite3 and flask.

1)install requirements(i.e with pip) 
	pip3 install sqlite3 
	pip3 install flask 

2)generate db file from script in scripts directory
	python3 create_passwords.py

3)app is ready to run: 
	python3 app.py

4)run show_schema.py to read electors and corresponding secret keys
	python3 show_schema.py 

5)open browser -> localhost:5000
	insert one of available elector_id and corresponding secre key 
	and choose candidate

6)admin view is accessible over localhost:5000/bar
	user: admin
	password: admin



db schema:
candidates(name text primary key)

electors(id integer primary key, secret_key text, vote text, date_of_vote text,
				 foreign key(vote) references candidates(name)); 
