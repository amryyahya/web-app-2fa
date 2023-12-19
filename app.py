from flask import Flask, render_template, request, make_response,redirect, url_for, session
from user import User
import os
from utils import generateLoginToken, verifyLoginToken, hashPassword, secretKeyGenerator, encryptSecretKey, decryptSecretKey, generateQrCode
from totp import getTOTP
from user_management import createTable, insertUser, getUser
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")

createTable()

@app.route('/')
def landingPage():
  email = verifyLoginToken(request.cookies.get('token')) 
  if email:
    return redirect(url_for('getDashboard'))
  return redirect(url_for('login'))

@app.route('/register',methods = ['GET','POST'])
def register():
  if request.method == 'GET':
    email = verifyLoginToken(request.cookies.get('token')) 
    if email:
      return redirect(url_for('getDashboard'))
    return render_template('register.html')
  email = request.form.get('email')
  name = request.form.get('name')
  address = request.form.get('address')
  phone_number = request.form.get('phone_number')
  password = request.form.get('password')
  confirmPassword = request.form.get('confirmPassword')
  secret_key = secretKeyGenerator()
  user = User(email, name, address, phone_number, hashPassword(password), encryptSecretKey(secret_key))
  if (insertUser(user)):
    if (confirmPassword!=password):
      return render_template('register.html',email=email,name=name,address=address,phone_number=phone_number,info="Password not Match")
    resp = make_response(redirect(url_for('getDashboard',info='Registration Success')))
    resp.set_cookie('token',generateLoginToken(email))
    return resp
  else:
    return render_template('register.html',email=email,name=name,address=address,phone_number=phone_number,info="Email has already Used")

@app.route('/login',methods = ['GET','POST'])
def login():
  if request.method == 'GET':
    email = verifyLoginToken(request.cookies.get('token'))
    if email:
      return redirect(url_for('getDashboard'))
    return render_template('login.html')
  email = request.form.get('email')
  password = request.form.get('password')
  hashedPassword = hashPassword(password)
  user = getUser(email)
  if not user:
    resp = render_template('login.html',info="Incorrect Email",email=email)
    return resp
  if hashedPassword == (user['password']):
    session['email'] = email
    resp = render_template('totp.html')
    return resp
  else:
    resp = render_template('login.html',info="Incorrect Password",email=email)
    return resp

@app.route('/dashboard',methods = ['GET','POST'])
def getDashboard():
  email = verifyLoginToken(request.cookies.get('token'))
  info = request.args.get('info', '')
  if not email:
    return redirect(url_for('login'))
  if request.method == 'GET':
    user = getUser(email) 
    resp = render_template('dashboard.html',info=info, email=user['email'],name=user['name'],address=user['address'],phone_number=user['phone_number'])
    return resp

@app.route('/2fa-setup',methods = ['GET','POST'])
def setTwoFactorAuth():
  email = verifyLoginToken(request.cookies.get('token'))
  if not email:
    return redirect(url_for('login'))
  if request.method == 'GET':
    user = getUser(email) 
    qrcode_image = generateQrCode(user)
    session['email'] = email
    return render_template('totp-setup.html', qrcode_image=qrcode_image)
  totp = request.form.get('totp')
  user = getUser(email)
  secret_key = decryptSecretKey(user['secret_key'])
  totp_verified = (totp == getTOTP(secret_key))
  if totp_verified:
    resp = make_response(redirect(url_for('getDashboard', info='Two-Factor Auth Setup Successfully')))
    return resp
  return "failed"

@app.route('/2fa-verify',methods = ['GET','POST'])
def verifyTwoFactorAuth():
  email = session['email'] 
  if not email:
    return redirect(url_for('login'))
  if request.method == 'GET':
    return render_template('totp.html')
  totp = request.form.get('totp')
  user = getUser(email)
  secret_key = decryptSecretKey(user['secret_key'])
  totp_verified = (totp == getTOTP(secret_key))
  if totp_verified:
    session.pop('email')
    info='Login Success'
    if (verifyLoginToken):
      info='Setup Success'
    resp = make_response(redirect(url_for('getDashboard',info=info)))
    resp.set_cookie('token',generateLoginToken(email))
    return resp
  return render_template('totp.html',info="Incorrect TOTP Code")

@app.route('/logout')
def logout():
  resp = make_response(redirect(url_for('login')))
  resp.set_cookie('token', '',expires=0)
  return resp

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=3000)