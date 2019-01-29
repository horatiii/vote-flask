from flask import Flask, render_template, request, url_for
import flask
import sqlite3
from sqltools import *

import flask_login

app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


users = {'admin': {'password': 'admin'}}
class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('bar'))

    return 'Bad login'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('logout.html')

@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect(flask.url_for('login')) 


@app.route('/',methods=['GET','POST'])
def home():
    if request.method == "POST":
        elector_id = request.form["elector"]
        secret_key = request.form['secret_key']
        option = request.form['options']
        print(elector_id, secret_key, option)
        print('credentials valid:',credentials_valid(elector_id,secret_key))
        print('data valid:',candidate_valid(option))
        if credentials_valid(elector_id, secret_key) and candidate_valid(option):

            if(can_vote(elector_id, secret_key)):
                if(make_vote(option, elector_id)): return render_template('success.html')
                else: return 'db connection error'
            else: return 'error: voted before' 

        else: return render_template('data_not_valid.html')



    elif request.method == 'GET':
        candidates=get_candidates()

        return render_template('home.html',candidates=candidates) 

    else: return 'wrong query'

@app.route('/bar')
@flask_login.login_required
def bar(): 
    labels, values = get_bar_values() 
    m = max(values) + 1 
    return render_template('bar.html', title='Voting results', maximum=m, labels=labels, values=values)



if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)# for development stage. It enables modify app.py on the fly
