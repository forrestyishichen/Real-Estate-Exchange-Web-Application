from flask import Flask, request, session, escape, g, abort, redirect, url_for, render_template, flash, current_app, jsonify, app
from flaskext.mysql import MySQL
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta



'''
init
'''
mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'any random string'
app.config['MYSQL_DATABASE_USER'] = 'ys'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ysys'
app.config['MYSQL_DATABASE_DB'] = 'teamfive'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


'''
Session Timeout
'''
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

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
    cursor.execute("SELECT property.property_id, property.status, \
        property.price, property_parameter.area from property inner \
        join property_parameter on property.property_id = \
        property_parameter.property_id")
    entries = []
    for i in range(3):
        row = cursor.fetchone()
        entries.append([row[0], row[1], row[2], row[3]])
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
    error = None
    if 'username' not in session:
        error = 'Please Login First'
        return render_template('login.html', error=error)
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * from property where owner_num = '{}'" .format(session['roleid']))
        entries = []
        for row in cursor.fetchall():
            entries.append([row[0], row[1]])
        cursor.close()
        return render_template('owenr_property.html', entries=entries)

'''
Property Register
'''

@app.route('/addproperty', methods=['GET', 'POST'])
def addproperty():
    error = None
    if request.methods == 'POST':
        property_id = request.form['property_id']
        asking_price = request.form['asking_price']
        room_num = request.form['room_num']
        bath_num = request.form['bath_num']
        garage_num = request.form['garage_num']
        lot_size = request.form['lot_size']
        zip_code = request.form['zip_code']
        area = request.form['area']
        list_date = request.form['list_date']

        if property_id == '' or owner_num == '':
            error = "Missing Information!"
            return render_template('owenr_property.html', error=error)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM property WHERE property_id='{}'" .format(property_id))
        data = cursor.fetchone()
        if data is not None:
            error = 'Duplicate Property ID!'
            cursor.close()
        else:
            conn.autocommit(False)
            try:
                cursor.execute("INSERT INTO user (ssn, user_name, password, bdate, address, email) VALUES('{}', '{}', '{}', '{}', '{}', '{}')" .format(ssn, username, hashed_password, bdate, address, email))
                cursor.execute("INSERT INTO name (user_name, fname, minit, lname) VALUES('{}', '{}', '{}', '{}')" .format(username, fname, minit, lname))
                conn.commit()
                cursor.close()
                flash('You Home were registered!')
            except:
                conn.rollback()    
    return render_template('owenr_property.html', error=error)

'''
Owner Page2 --- Offer managerment
'''
@app.route('/owneroffer', methods=['GET', 'POST'])
def owner_offer():
    error = None
    if 'username' not in session:
        error = 'Please Login First'
        return render_template('login.html', error=error)
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT offer.property_id, offer.offer_num, offer.price, offer.offer_date, offer.agent_num \
            from offer inner join property on offer.property_id = property.property_id \
            where property.owner_num = '{}'".format(session['roleid']))
        entries = []
        for row in cursor.fetchall():
            entries.append([row[0], row[1], row[2], row[3], row[4]])
        cursor.close()
        return render_template('owner_offer.html', entries=entries)

'''
Agent Page1 --- Add Openhouse and list Openhouse
'''
@app.route('/agentopenhouse' , methods=['GET', 'POST'])
def agent_openhouse():
    error = None
    if 'username' not in session:
        error = 'Please Login First'
        return render_template('login.html', error=error)
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT oh_num, property_id, start_date, end_date  \
            FROM open_house WHERE agent_num = '{}'".format(session['roleid']))
        entries = []
        for row in cursor.fetchall():
            entries.append([row[0], row[1], row[2]]) 
        cursor.close()
        return render_template('agent_openhouse.html', entries=entries)

'''
Agent Page2 --- Commision managerment
'''
@app.route('/agentcommision', methods=['GET', 'POST'])
def agent_commision():
    error = None
    if 'username' not in session:
        error = 'Please Login First'
        return render_template('login.html', error=error)
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT total_commission, commission_rate \
            FROM agent WHERE agent_num = '{}'".format(session['roleid']))
        entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
        cursor.close()
        return render_template('agent_commision.html', entries=entries)

'''
Buyer Page1 --- Add offer and list offer
'''
@app.route('/buyeroffer/', methods=['GET', 'POST'])
@app.route('/buyeroffer/<prperty_id>', methods=['GET', 'POST'])
def buyer_offer(prperty_id=''):
    error = None
    if 'username' not in session:
        error = 'Please Login First'
        return render_template('login.html', error=error)
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT offer_num, property_id, price, offer_date, status, agent_num \
            FROM offer WHERE buyer_num = '{}'".format(session['roleid']))
        entries = []
        for row in cursor.fetchall():
            entries.append([row[0], row[1], row[2], row[3], row[4], row[5]]) 
        cursor.close()
        return render_template('buyer_offer.html', entries=entries, id=id)

'''
Buyer Page2 --- Open House managerment
'''
@app.route('/buyeropenhouse', methods=['GET', 'POST'])
def buyer_openhouse():
    error = None
    if 'username' not in session:
        error = 'Please Login First'
        return render_template('login.html', error=error)
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT oh.agent_num, property_id, start_date, end_date \
            FROM open_house oh, oh_visit ohv\
            WHERE oh.agent_num = ohv.agent_num \
                AND oh.oh_num = ohv.oh_num \
                AND ohv.buyer_num = '{}'".format(session['username']))
        entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
        cursor.close()
        return render_template('buyer_openhouse.html', entries=entries)


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
User Login
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
        cursor.execute("SELECT password, ssn from user where user_name= '{}'" .format(username))
        data = cursor.fetchone()
        if data == None:
            error = 'Invalid username and password'
        elif check_password_hash(data[0], password):
            session['logged_in'] = True
            session['username'] = username
            session['rolename'] = role
            session['ssn'] = data[1]
            '''
            Register to role table
            '''
            cursor.execute("SELECT {} FROM {} WHERE ssn = '{}'" .format((role+'_num'), role, session['ssn']))
            data = cursor.fetchone()
            if data is None:
                cursor.execute("SELECT count(*) FROM {}" .format(role))
                num = cursor.fetchone()
                cursor.execute("INSERT INTO {} ({}, ssn) VALUES('{}', '{}')" .format(role,(role+'_num'),(role+'_'+str(num[0]+1)), session['ssn']))
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
User Register
'''

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ssn = request.form['ssn']
        fname = request.form['fname']
        minit = request.form['minit']
        lname = request.form['lname']
        bdate = request.form['bdate']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        hashed_password = generate_password_hash(password)

        '''
        Empty check
        '''
        if username == '' or password == '' or ssn == '' or email == '':
            error = "Missing Information!"
            return render_template('register.html', error=error)

        '''
        Duplicate check
        '''
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE user_name='{}'" .format(username))
        data = cursor.fetchone()
        if data is not None:
            error = 'Duplicate username and password'
            cursor.close()
        else:
            '''
            Transaction
            '''
            conn.autocommit(False)
            try:
                cursor.execute("INSERT INTO user (ssn, user_name, password, bdate, address, email) VALUES('{}', '{}', '{}', '{}', '{}', '{}')" .format(ssn, username, hashed_password, bdate, address, email))
                cursor.execute("INSERT INTO name (user_name, fname, minit, lname) VALUES('{}', '{}', '{}', '{}')" .format(username, fname, minit, lname))
                conn.commit()
                cursor.close()
                flash('You were registered, %s' % escape(username))
                return render_template('login.html', error=error)
            except:
                conn.rollback()    
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
    session.pop('ssn', None)
    flash('You were logged out')
    return redirect(url_for('login'))



'''
Detail page
TO DO **** list detail and action
'''

@app.route('/entity/<property_id>', methods=['GET'])
def show_property_profile(property_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT property.property_id, property.status, \
        property.price, property_parameter.room_num, property_parameter.bath_num, \
        property_parameter.garage_num, property_parameter.lot_size, \
        property_parameter.zip_code, property_parameter.area from property inner \
        join property_parameter on property.property_id = \
        property_parameter.property_id where property.property_id = '{}'" .format(property_id))

    entries = []
    for row in cursor.fetchall():
        entries.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
    cursor.close()
    return render_template('property_detail.html', entries=entries)

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


