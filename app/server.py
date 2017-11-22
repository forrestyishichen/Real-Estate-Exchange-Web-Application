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
Index Page
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
Main Page 1 --- Property Search with recommendation
'''

@app.route('/search_property', methods=['GET', 'POST'])
def search_property():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from user")
    entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
    cursor.close()
    return render_template('search_property.html', entries=entries)

'''
Main Page 2 --- Open House Search
'''

@app.route('/searchopenhouse', methods=['GET', 'POST'])
def search_openhouse():
    return render_template('search_openhouse.html')
    # return render_template('search_openhouse.html', entries=entries)

'''
Main Page 3 --- Market Report
'''

# @app.route('/marketreport', methods=['GET'])
# def market_report():
#     return render_template('market_report.html')

'''
Owner Page1 --- Add property and list property
'''
@app.route('/ownerproperty' , methods=['GET', 'POST'])
def owner_property():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from user where username = '{}'".format(session['username']))
    entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
    cursor.close()
    return render_template('owenr_property.html', entries=entries)

'''
Owner Page2 --- Offer managerment
'''
@app.route('/owneroffer', methods=['GET', 'POST'])
def owner_offer():
    return render_template('owner_offer.html')

'''
Agent Page1 --- Add Openhouse and list Openhouse
'''
@app.route('/agentopenhouse' , methods=['GET', 'POST'])
def agent_openhouse():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from user where username = '{}'".format(session['username']))
    entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
    cursor.close()
    return render_template('agent_openhouse.html', entries=entries)

'''
Agent Page2 --- Commision managerment
'''
@app.route('/agentcommision', methods=['GET', 'POST'])
def agent_commision():
    return render_template('agent_commision.html')

'''
Buyer Page1 --- Add offer and list offer
'''
@app.route('/buyeroffer' , methods=['GET', 'POST'])
def buyer_offer():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from user where username = '{}'".format(session['username']))
    entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
    cursor.close()
    return render_template('buyer_offer.html', entries=entries)

'''
Buyer Page2 --- Open House managerment
'''
@app.route('/buyeropenhouse', methods=['GET', 'POST'])
def buyer_openhouse():
    return render_template('buyer_openhouse.html')


'''
Search funtion
TO DO **** transaction, add 
'''

# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     g.db.execute('insert into entries (title, text) values (?, ?)',
#                  [request.form['title'], request.form['text']])
#     g.db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))

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
            session['rolename'] = role

            '''
            Register to role table
            '''
            cursor.execute("SELECT {} FROM {} WHERE ssn = '{}'" .format((role+'_num'), role, username))
            data = cursor.fetchone()
            if data is None:
                cursor.execute("SELECT count(*) FROM {}" .format(role))
                num = cursor.fetchone()
                cursor.execute("INSERT INTO {} ({}, ssn) VALUES('{}', '{}')" .format(role,(role+'_num'),(role+'_'+str(num[0]+1)), username))
                conn.commit()
                session['roleid'] = (role+'_'+str(num[0]+1))
                flash('Register as %s' % escape(session['rolename']))
            else:
                session['roleid'] = data[0]
                flash('Login as %s' % escape(session['rolename']))
            cursor.close()
            return redirect(url_for('search_property'))
        else:
            cursor.close()
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
        cursor.execute("SELECT Username FROM User WHERE Username='" + username + "'")
        data = cursor.fetchone()
        if data is not None:
            error = 'Duplicate username and password'
            cursor.close()
        else:
            cursor.execute('''INSERT INTO User (userName, password) VALUES(%s, %s)''', (username, hashed_password))
            conn.commit()
            cursor.close()
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
    session.pop('rolename', None)
    session.pop('roleid', None)
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
    cursor.close()
    if data is None:
     return "User not found"
    else:
     return data

'''
404
'''

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

'''
Main
'''

if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0',port=5000)


