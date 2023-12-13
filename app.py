from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for
from user import User
from user_management import createTable, insertUser, editUser, getAllUsers, getUser
import hashlib

createTable()

app = Flask(__name__)

@app.route('/')
def landingPage():
  return render_template('landingPage.html')

@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'GET':
      return render_template('register.html')
    email = request.form.get('email')
    name = request.form.get('name')
    address = request.form.get('address')
    phone_number = request.form.get('phone_number')
    password = request.form.get('password')
    confirmPassword = request.form.get('confirmPassword')
    if (confirmPassword!=password):
      return '<h3>Password not match</h3>'
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    hashedPassword = sha256_hash.hexdigest()
    user = User(email, name, address, phone_number, hashedPassword)
    if (insertUser(user)):
      return '<h3>Registration Succeed!</h3> <br> <a href="/login">Login</a>'
    else:
      return '<h3>Registration Failed! Email is Used</h3>'

@app.route('/update',methods = ['POST'])
def update():
    email = request.form.get('email')
    name = request.form.get('name')
    address = request.form.get('address')
    phone_number = request.form.get('phone_number')
    password = request.form.get('password')
    confirmPassword = request.form.get('confirmPassword')
    if (confirmPassword!=password):
      return '<h3>Password not match</h3>'
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    hashedPassword = sha256_hash.hexdigest()
    user = User(email, name, address, phone_number, hashedPassword)
    if (editUser(user)):
      return '<h3>Update Succeed!</h3> <br> <a href="/login">Login</a>'
    else:
      return '<h3>Update Failed! Email is Used</h3>'

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'GET':
      user_email = request.cookies.get('user_email') 
      if user_email is not None:
         return redirect(url_for('dashboard'))
      return render_template('login.html')
    email = request.form.get('email')
    password = request.form.get('password')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    hashedPassword = sha256_hash.hexdigest()
    user = getUser(email)
    if user[4] == hashedPassword:
      resp = make_response(redirect(url_for('dashboard')))
      resp.set_cookie('user_email',email)
      return resp
    else:
      return "<h3>wrong password/email</h3>"

@app.route('/dashboard',methods = ['GET','POST'])
def dashboard():
    if request.method == 'GET':
      user_email = request.cookies.get('user_email') 
      if user_email is None:
         return redirect(url_for('login'))
      user = getUser(user_email) 
      return render_template('dashboard.html', email=user[0],name=user[1],address=user[2],phone_number=user[3])

@app.route('/database')
def database():
    users = getAllUsers()
    users_list = []
    for user in users:
      users_list.append({
          'email': user.email,
          'name': user.name,
          'address': user.address,
          'phone_number': user.phone_number,
          'password': user.password
      })
    return jsonify(users_list)

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('user_email', '', expires=0)
    return resp


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
