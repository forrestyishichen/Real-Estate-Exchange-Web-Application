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
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '880112'
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
Main Page 1 --- Property Search with recommendation
'''

@app.route('/search_property', methods=['GET', 'POST'])
def search_property():
    conn = mysql.connect()
    cursor = conn.cursor()
    q = "SELECT property.property_id, property.status, \
        property.price, property_parameter.area from property inner \
        join property_parameter on property.property_id = \
        property_parameter.property_id"
    cursor.execute(q)
    entries = []
    for i in range(3):
        row = cursor.fetchone()
        entries.append([row[0], row[1], row[2], row[3]])
    cursor.close()
    return render_template('search_property.html', entries=entries)

'''
Search Property
'''

@app.route('/p_search', methods=['Get', 'POST'])
def p_search():
    error = None
    if request.method == 'POST':
        lowprice = request.form['lowprice']
        highprice = request.form['highprice']
        area = request.form['area']
        room_num = request.form['room_num']
        bath_num = request.form['bath_num']
        garage_num = request.form['garage_num']

        entries = []

        if not is_number(lowprice) and lowprice != '':
            error = "Please provide a valid price!"
        elif not is_number(highprice) and highprice != '':
            error = "Please provide a valid price!"
        elif not is_number(room_num) and room_num != '':
            error = "Please provide a valid room_num number!"
        elif not is_number(bath_num) and bath_num != '':
            error = "Please provide a valid bath_num number!"
        elif not is_number(garage_num) and garage_num != '':
            error = "Please provide a valid garage_num number!"
        else:
            myquery = "SELECT property.property_id, property.status, property.asking_price, property_parameter.area \
                      FROM property, property_parameter \
                      WHERE property.property_id = property_parameter.property_id"

            if lowprice == '':
                lowprice = 0

            if highprice == '':
                highprice = 999999999

            priceq = " AND price >= {} AND price <= {}".format(lowprice, highprice)
            myquery = myquery + priceq  

            if area != '':
                addsq = " AND area = '{}'".format(area)
                myquery = myquery + addsq

            if room_num != '':
                addsq = " AND property_parameter.room_num = {}".format(room_num)
                myquery = myquery + addsq

            if bath_num != '':
                addsq = " AND property_parameter.bath_num = {}".format(bath_num)
                myquery = myquery + addsq

            if garage_num != '':
                addsq = " AND property_parameter.garage_num = {}".format(garage_num)
                myquery = myquery + addsq

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(myquery)

            for row in cursor.fetchall():
                entries.append([row[0], row[1], row[2], row[3]])
                cursor.close()

        return render_template('search_property.html', entries=entries, error=error)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


'''
Main Page 2 --- Open House Search
'''

@app.route('/searchopenhouse', methods=['GET', 'POST'])
def search_openhouse():
    error = None
    entries =[]
    return render_template('search_openhouse.html', entries=entries, error=error)

'''
Search Open House
'''

@app.route('/o_search', methods=['GET', 'POST'])
def o_search():
    error = None
    if request.method == 'POST':
        lowprice = request.form['lowprice']
        highprice = request.form['highprice']
        area = request.form['area']
        room_num = request.form['room_num']
        bath_num = request.form['bath_num']
        garage_num = request.form['garage_num']

        entries = []

        if not is_number(lowprice) and lowprice != '':
            error = "Please provide a valid price!"
        elif not is_number(highprice) and highprice != '':
            error = "Please provide a valid price!"
        elif not is_number(room_num) and room_num != '':
            error = "Please provide a valid room_num number!"
        elif not is_number(bath_num) and bath_num != '':
            error = "Please provide a valid bath_num number!"
        elif not is_number(garage_num) and garage_num != '':
            error = "Please provide a valid garage_num number!"
        else:
            myquery = "SELECT open_house.oh_num, open_house.property_id, \
                       open_house.start_date, open_house.end_date, property.asking_price \
                      FROM open_house, property \
                      WHERE open_house.property_id = property.property_id"

            if lowprice == '':
                lowprice = 0

            if highprice == '':
                highprice = 999999999

            priceq = " AND price >= {} AND price <= {}".format(lowprice, highprice)
            myquery = myquery + priceq

            if area != '':
                addsq = " AND area = '{}'".format(area)
                myquery = myquery + addsq

            if room_num != '':
                addsq = " AND property_parameter.room_num = {}".format(room_num)
                myquery = myquery + addsq

            if bath_num != '':
                addsq = " AND property_parameter.bath_num = {}".format(bath_num)
                myquery = myquery + addsq

            if garage_num != '':
                addsq = " AND property_parameter.garage_num = {}".format(garage_num)
                myquery = myquery + addsq

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(myquery)

            for row in cursor.fetchall():
                entries.append([row[0], row[1], row[2], row[3], row[4]])
                cursor.close()

    return render_template('search_openhouse.html', entries=entries, error=error)

'''
Open House Visit
'''
@app.route('/ohvisit/<oh_num>', methods=['GET', 'POST'])
def ohvisit(oh_num):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT agent_num FROM open_house \
        WHERE oh_num='{}'" .format(oh_num))
    data = cursor.fetchone()
    myagent = data[0]

    conn.autocommit(False)
    try:
        cursor.execute("INSERT INTO oh_visit (buyer_num, agent_num, \
            oh_num) VALUES('{}', '{}', '{}' \
            )" .format(session['roleid'], myagent, oh_num))
        conn.commit()
        cursor.close()
        flash('Thank you for visiting!')
    except:
        flash('There are some errors!')
        conn.rollback()    
    return redirect(url_for('buyer_openhouse'))

'''
Main Page 3 --- Market Report
'''

@app.route('/market_report', methods=['GET'])
def market_report():
    q = []
    # total sold properties
    q.append("SELECT Count(*) FROM property WHERE status = 'Sold'")
    # total onsale properties
    q.append("SELECT Count(*) FROM property WHERE status = 'On Sale'")
    # total openhouses
    q.append("SELECT Count(*) FROM open_house")
    # lowest onsale price
    q.append("SELECT asking_price FROM property WHERE status = 'On Sale' ORDER BY price LIMIT 1")
    # highest onsale price
    q.append("SELECT asking_price FROM property WHERE status = 'On Sale' ORDER BY price DESC LIMIT 1")
    # average onsale price
    q.append("SELECT Avg(asking_price) FROM property WHERE status = 'On Sale'")
    # lowest sold price
    q.append("SELECT price FROM property WHERE status = 'Sold' ORDER BY price LIMIT 1")
    # highest sold price
    q.append("SELECT price FROM property WHERE status = 'Sold' ORDER BY price DESC LIMIT 1")
    # average sold price
    q.append("SELECT Avg(price) FROM property WHERE status = 'Sold'")

    conn = mysql.connect()
    cursor = conn.cursor()
    res = []
    for sq in q:
        cursor.execute(sq)
        r = cursor.fetchone()
        if r[0] is None:
            r[0] = "NULL"
        if is_number(r[0]):
            res.append(int(r[0]))
        else:
            res.append(r[0])

    entries = []
    entries.append(res)
    return render_template('market_report.html', entries=entries)

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
        cursor.execute("SELECT property_id, status, list_date from property where owner_num = '{}'" .format(session['roleid']))
        entries = []
        for row in cursor.fetchall():
            entries.append([row[0], row[1], row[2]])
        cursor.close()
        return render_template('owenr_property.html', entries=entries)

'''
Property Register
'''

@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    error = None
    if request.method == 'POST':
        property_id = request.form['property_id']
        asking_price = request.form['asking_price']
        room_num = request.form['room_num']
        bath_num = request.form['bath_num']
        garage_num = request.form['garage_num']
        lot_size = request.form['lot_size']
        zip_code = request.form['zip_code']
        area = request.form['area']
        list_date = request.form['list_date']

        if property_id == '':
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
                cursor.execute("INSERT INTO property (property_id, status, \
                    asking_price, list_date, owner_num) VALUES('{}', 'On Sale', \
                     '{}', '{}', '{}')" .format(property_id, asking_price, list_date, session['roleid']))
                cursor.execute("INSERT INTO property_parameter (property_id, \
                    room_num, bath_num, garage_num, lot_size, zip_code, area) \
                    VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')" .format(property_id, \
                     room_num, bath_num, garage_num, lot_size, zip_code, area))
                conn.commit()
                cursor.close()
                flash('You Home were registered!')
            except:
                error = 'There are some errors!'
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
        cursor.execute("SELECT offer.property_id, offer.offer_num, offer.price, \
            offer.offer_date, offer.agent_num, offer.status \
            from offer inner join property on offer.property_id = property.property_id \
            where property.owner_num = '{}'".format(session['roleid']))
        entries = []
        for row in cursor.fetchall():
            entries.append([row[0], row[1], row[2], row[3], row[4], row[5]])
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
            entries.append([row[0], row[1], row[2], row[3]]) 
        cursor.close()
        return render_template('agent_openhouse.html', entries=entries)

'''
Open House Register
'''

@app.route('/add_openhouse', methods=['GET', 'POST'])
def add_openhouse():
    error = None
    if request.method == 'POST':
        property_id = request.form['property_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        if property_id == '' or start_date == '' or end_date == '':
            error = "Missing Information!"
            return render_template('agent_openhouse.html', error=error)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT property_id, status, agent_num \
            FROM property WHERE property_id='{}'" .format(property_id))
        data = cursor.fetchone()
        if data is None:
            error = 'No such home!'
            cursor.close()
        elif data[1] == 'Sold':
            error = 'Already Sold!'
            cursor.close()
        elif data[2] is not None:
            error = 'Already registered an Open House!'
            cursor.close()
        else:
            cursor.execute("SELECT count(*) FROM open_house")
            num = cursor.fetchone()
            conn.autocommit(False)
            try:
                cursor.execute("INSERT INTO open_house (agent_num, oh_num, \
                    start_date, end_date, property_id) VALUES('{}', '{}', \
                     '{}', '{}', '{}')" .format(session["roleid"], \
                        ('oh_' + str(num[0] + 1)), start_date, end_date, property_id))
                conn.commit()
                cursor.close()
                flash('You Open House were registered!')
                return redirect(url_for('agent_openhouse'))
            except:
                error = 'There are some errors!'
                conn.rollback()    
    return render_template('agent_openhouse.html', error=error)

'''
Agent Page2 --- Commision managerment
'''

@app.route('/agent_commision', methods=['GET', 'POST'])
def agent_commision():
    error = None
    if 'username' not in session:
        error = 'Please Login First'
        return render_template('login.html', error=error)
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT count(offer.status)\
            FROM offer WHERE offer.agent_num = '{}' \
            AND offer.status = 'Deal'".format(session['roleid']))
        data1=cursor.fetchone()
        cursor.execute("SELECT total_commission FROM agent \
            where agent_num = '{}'" .format(session['roleid']))
        data2=cursor.fetchone()
        if data2[0] == None:
            data2 = list(data2)
            data2[0] = 0.00
            data2 = tuple(data2)
        entries =[] 
        entries.append([data1[0],data2[0]])
        cursor.close()
        return render_template('agent_commision.html', entries=entries)

'''
Buyer Page1 --- Add offer and list offer
'''

@app.route('/buyeroffer', methods=['GET', 'POST'])
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
        return render_template('buyer_offer.html', entries=entries, id=prperty_id)

'''
Offer Register
'''

@app.route('/add_offer', methods=['GET', 'POST'])
def add_offer():
    error = None
    if request.method == 'POST':
        property_id = request.form['property_id']
        price = request.form['price']
        offer_date = request.form['offer_date']

        if property_id == '' or price == '' or offer_date == '':
            error = "Missing Information!"
            return render_template('buyer_offer.html', error=error)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT property.status, owner.ssn, property.agent_num \
            FROM property inner join owner on property.owner_num = owner.owner_num \
            WHERE property.property_id='{}'" .format(property_id))
        data = cursor.fetchone()
        if data is None:
            error = 'No such home!'
            cursor.close()
        elif data[0] == 'Sold':
            error = 'Already Sold!'
            cursor.close()
        elif data[1] == session['ssn']:
            error = 'This is your own House!'
            cursor.close()
        else:
            agent_num = data[2]
            cursor.execute("SELECT count(*) FROM offer")
            num = cursor.fetchone()
            conn.autocommit(False)
            try:
                cursor.execute("INSERT INTO offer (buyer_num, offer_num, \
                    price, status, offer_date, property_id, agent_num) VALUES('{}', '{}', \
                     '{}', 'Progress', '{}', '{}', '{}')" .format(session["roleid"], \
                        ('offer_' + str(num[0] + 1)), price, offer_date, property_id, agent_num))
                conn.commit()
                cursor.close()
                flash('You Offer were registered!')
                return redirect(url_for('buyer_offer'))
            except:
                error = 'There are some errors!'
                conn.rollback()    
    return render_template('buyer_offer.html', error=error)

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
        cursor.execute("SELECT property_id, oh.agent_num, end_date \
            FROM open_house oh, oh_visit ohv\
            WHERE oh.agent_num = ohv.agent_num \
                AND oh.oh_num = ohv.oh_num \
                AND ohv.buyer_num = '{}'".format(session['roleid']))
        entries = []
        for row in cursor.fetchall():
            entries.append([row[0], row[1], row[2]]) 
        cursor.close()
        return render_template('buyer_openhouse.html', entries=entries)

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
Accept Offer
'''

@app.route('/accept_offer/<offer_num>', methods=['GET', 'POST'])
def accept_offer(offer_num):
    error = None
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT property.status, offer.status FROM property inner join offer on \
            property.property_id = offer.property_id WHERE offer.offer_num='{}'" .format(offer_num))
        data = cursor.fetchone()
        if data[0] == 'Sold':
            cursor.close()
            flash('House Already Sold!!')
        elif data[0] == 'Deal':
            cursor.close()
            flash('Offer Already Accepted!!')
        else:
            cursor.execute("SELECT property_id, price, agent_num FROM offer \
                WHERE offer_num='{}'" .format(offer_num))
            data = cursor.fetchone()
            newid = data[0]
            newprice = data[1]
            newagent = data[2]

            cursor.execute("SELECT total_commission FROM agent \
                WHERE agent_num='{}'" .format(newagent))
            data = cursor.fetchone()
            newtotal = data[0]
            newtotal = float(newtotal) + (float(newprice)*0.03)

            conn.autocommit(False)
            try:
                cursor.execute("UPDATE property SET status = 'Sold', price = '{}' \
                    WHERE property_id ='{}'" .format(newprice,newid))
                cursor.execute("UPDATE offer SET status = 'Deal' \
                    WHERE offer_num ='{}'" .format(offer_num))
                cursor.execute("UPDATE agent SET total_commission = {}, commission_rate = 0.03\
                    WHERE agent_num ='{}'" .format(newtotal,newagent))
                conn.commit()
                cursor.close()
                flash('Congratulations, %s!' % escape(username))
            except:
                flash('House Already Sold!!')
                conn.rollback()
    return redirect(url_for('owner_offer'))

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