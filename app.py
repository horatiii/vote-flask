""" Main script with flask initialization """
from flask import Flask, \
                  request, \
                  redirect, \
                  url_for, \
                  render_template

from flask_login import login_user, \
                        logout_user, \
                        login_required, \
                        LoginManager, \
                        UserMixin

from sqltools import get_bar_values, \
                     get_candidates, \
                     credentials_valid, \
                     can_vote, \
                     candidate_valid, \
                     make_vote

app = Flask(__name__)
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(app)

USERS = {'admin': {'password': 'admin'}}


""" user Class """
class User(UserMixin):
    pass


# """ user loader """
@LOGIN_MANAGER.user_loader
def user_loader(email):
    if email not in USERS:
        return

    user = User()
    user.id = email
    return user


""" request loader """
@LOGIN_MANAGER.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in USERS:
        return

    user = User()
    user.id = email
    user.is_authenticated = request.form['password'] == USERS[email]['password']
    return user


""" route /login """
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    if request.form['password'] == USERS[email]['password']:
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for('hidden'))

    return 'Bad login'


""" route /logout """
@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html')

"""
unauthorized handler
"""
@LOGIN_MANAGER.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

""" route / """
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        elector_id = request.form["elector"]
        secret_key = request.form['secret_key']
        option = request.form['options']
        if credentials_valid(elector_id, secret_key) and candidate_valid(option):

            if can_vote(elector_id, secret_key):
                if make_vote(option, elector_id): return render_template('success.html')
                else: return 'db connection error'
            else: return 'error: voted before'

        else: return render_template('data_not_valid.html')

    if request.method == 'GET':
        candidates = get_candidates() 
        return render_template('home.html', candidates=candidates)

    else: return 'wrong query'

""" route /hidden """
@app.route('/hidden')
@login_required
def hidden():
    labels, values = get_bar_values()
    maximum = max(values) + 1
    return render_template('bar.html',
                           title='Voting results',
                           maximum=maximum,
                           labels=labels,
                           values=values)



if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)# for development stage. It enables modify app.py on the fly
