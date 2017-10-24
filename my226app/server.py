from flask import Flask
from flask import current_app
from flask import render_template
from flask import abort, redirect, url_for
from flask import request
from flask import jsonify
from flaskext.mysql import MySQL
import json

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '880112'
app.config['MYSQL_DATABASE_DB'] = 'mydata'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def index():
    return current_app.send_static_file('index.html')
      # return redirect(url_for('login'))

@app.route('/<string:page_name>/')
def static_page(page_name):
    return current_app.send_static_file('%s.html' % page_name)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User")
    mydata = json.dumps(cursor.fetchall())
    return render_template('hello.html', name=mydata)

# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return 'User %s' % username

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id

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

@app.route("/Alluser", methods=['GET'])
def Alluser():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User")
    return jsonify(data=cursor.fetchall())

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     # the code below is executed if the request method
#     # was GET or the credentials were invalid
#     return render_template('login.html', error=error)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0',port=5000)


# url_for('static', filename='style.css')


