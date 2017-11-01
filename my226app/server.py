from flask import Flask, request, session, g, abort, redirect, url_for, render_template, flash, current_app, jsonify
from flaskext.mysql import MySQL
import json

'''
database
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
    return current_app.send_static_file('index.html')

'''
Static page
'''

@app.route('/<string:page_name>/')
def static_page(page_name):
    return current_app.send_static_file('%s.html' % page_name)

'''
Old output
'''

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User")
    # mydata = json.dumps(cursor.fetchall())
    # mydata = [dict(username=row[0], password=row[1]) for row in cursor.fetchall()]
    mydata = cursor.fetchall()
    return render_template('hello.html', name=mydata)

'''
New output
'''

@app.route('/show')
def show_entries():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User")
    # cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
    return render_template('show_entries.html', entries=entries)

'''
New input
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
New login
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            error = 'Invalid username and password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
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
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT Username from User where Username='" + username + "'")
        data = cursor.fetchone()
        if data is not None:
            error = 'Duplicate username and password'
        else:
            cursor.execute('''INSERT INTO User (userName, password) VALUES(%s, %s)''', (username, password))
            conn.commit()
            session['logged_in'] = True
            flash('You were registered')
            return redirect(url_for('show_entries'))
    return render_template('register.html', error=error)

'''
Login out
'''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


'''
Single user page
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

# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return 'User %s' % username

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id

'''
Old Login Section
'''
@app.route("/Authenticate", methods=['GET'])
def Authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return current_app.send_static_file('loginfailed.html')
    else:
     return current_app.send_static_file('loginok.html')

@app.route("/Newuseradder")
def Newuseradder():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    print(username)
    print(password)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO User (userName, password) VALUES(%s, %s)''', (username, password))
    conn.commit()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0',port=5000)


