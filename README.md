Voting system built in python3 with use of sqlite3 and flask. <br/>


1)install requirements(i.e with pip) <br/>
	pip3 install sqlite3 <br/>
	pip3 install flask <br/>

2)generate db file from script in scripts directory<br/>
	python3 create_passwords.py<br/>

3)app is ready to run: <br/>
	python3 app.py<br/>

4)run show_schema.py to read electors and corresponding secret keys<br/>
	python3 show_schema.py <br/>

5)open browser -> localhost:5000<br/>
	insert one of available elector_id and corresponding secre key <br/>
	and choose candidate<br/>

6)admin view is accessible over localhost:5000/bar<br/>
	user: admin<br/>
	password: admin<br/>

<br/><br/>

db schema:<br/>

candidates(name text primary key)<br/>
<br/>

electors(id integer primary key, secret_key text, vote text, date_of_vote text,<br/>
				 foreign key(vote) references candidates(name)); <br/>
