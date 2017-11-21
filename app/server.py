from flask import Flask, request, session, escape, g, abort, redirect, url_for, render_template, flash, current_app, jsonify
from flaskext.mysql import MySQL
import json
from werkzeug.security import generate_password_hash, check_password_hash

'''
init
'''
mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'any random string'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '880112'
app.config['MYSQL_DATABASE_DB'] = 'mydata'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

'''
Index
'''

@app.route('/')
def index():
    return render_template('login.html')
    # return current_app.send_static_file('index.html')

'''
Static page
'''

@app.route('/<string:page_name>/')
def static_page(page_name):
    return current_app.send_static_file('%s.html' % page_name)

'''
Main Page --- Market Report with Search
'''

@app.route('/show')
def show_entries():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from User")
    # cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
    return render_template('show_entries.html', entries=entries)

'''
Input
TO DO **** transaction, add 
'''

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

'''
Login
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        '''
        Validation
        '''
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT password from User where Username='" + username + "'")
        data = cursor.fetchone()
        if check_password_hash(data[0], password):
            session['logged_in'] = True
            session['username'] = username
            session['role'] = role
            flash('Logged in as %s' % escape(session['role']))
            return redirect(url_for('show_entries'))
        else:
            error = 'Invalid username and password'
    return render_template('login.html', error=error)

'''
Register
'''

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        '''
        Add more
        '''

        '''
        Empty check
        '''
        if username == '' or password == '':
            error = "Missing Information!"
            return render_template('register.html', error=error)

        '''
        Duplicate check
        '''
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT Username from User where Username='" + username + "'")
        data = cursor.fetchone()
        if data is not None:
            error = 'Duplicate username and password'
        else:
            cursor.execute('''INSERT INTO User (userName, password) VALUES(%s, %s)''', (username, hashed_password))
            conn.commit()
            flash('You were registered, %s' % escape(username))
            return render_template('login.html', error=error)
    return render_template('register.html', error=error)

'''
Logout
'''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('login'))



'''
Detail page
TO DO **** list detail and action
'''

@app.route('/user/<username>', methods=['GET'])
def show_user_profile(username):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where Username='" + username + "'")
    data = cursor.fetchone()
    if data is None:
     return "User not found"
    else:
     return data

'''
Error
TO DO **** add a template
'''

@app.errorhandler(404)
def page_not_found(error):
    return "404 page_not_found" , 404
    # return render_template('page_not_found.html'), 404


'''
Main
'''

if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0',port=5000)


