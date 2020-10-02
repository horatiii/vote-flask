# Voting system built in python3 with use of sqlite3 and flask. <br/>

![Alt text](img/make_vote.png?raw=true "make vote")

![Alt text](img/login.png?raw=true "login")

![Alt text](img/results.png?raw=true "results")
1. install requirements(i.e with pip)
	-	`pip install flask flask_login` 
<br/><br/>

2. generate db file from script in scripts directory
	-  `python3 create_passwords.py`
<br/><br/>

3. app is ready to run:
	- `python3 app.py`
<br/><br/>

4. run show_scheme.py to read electors id and corresponding secret keys
	-  `python3 show_schema.py`
<br/><br/>

5. open browser -> localhost:5000
	-  insert one of available elector_id and corresponding secret key
  and choose candidate (A, B or C)
<br/><br/>

6. admin view is accessible over localhost:5000/login
	- user: admin
	- password: admin
<br/><br/>
<br/><br/>


db schema:
 candidates(name text primary key)
 electors(id integer primary key, secret_key text, vote text, date_of_vote text,
				 foreign key(vote) references candidates(name));
