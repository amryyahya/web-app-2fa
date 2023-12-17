import hashlib, qrcode, io, os, base64, string, random, jwt, datetime
from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for, send_file, session
from user import User
from totp import getTOTP
from user_management import createTable, insertUser, editUser, getAllUsers, getUser
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

createTable()

app = Flask(__name__)

def generateLoginToken(email, two_factor=False):
  expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=3)
  payload = {
    "email": email,
    "exp": expiration_time
  }
  secret_key = os.environ.get("JWT_SECRET_KEY")
  return jwt.encode(payload, secret_key, algorithm="HS256")

def verifyLoginToken():
  if request.cookies.get('token') is None:
    return False
  try:
    token = request.cookies.get('token') 
    secret_key = os.environ.get("JWT_SECRET_KEY")
    decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    email = decoded_payload['email']
    return email
  except jwt.ExpiredSignatureError:
    return False, {"error": "Token has expired"}
  except jwt.InvalidTokenError:
    return False, {"error": "Invalid token"}

def hashPassword(password):
  sha256_hash = hashlib.sha256()
  sha256_hash.update(password.encode('utf-8'))
  hashedPassword = sha256_hash.hexdigest()
  return hashedPassword

def secretKeyGenerator():
  characters = string.ascii_letters + string.digits
  secret_key = ''.join(random.choice(characters) for i in range(16)).encode('utf-8')
  return secret_key

def encryptSecretKey(plain):
  key = os.environ.get("AES_SECRET_KEY").encode('utf-8')
  iv = os.environ.get("AES_INITIAL_VECTOR").encode('utf-8')
  padder = padding.PKCS7(algorithms.AES.block_size).padder()
  padded_plaintext = padder.update(plain) + padder.finalize()
  cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
  encryptor = cipher.encryptor()
  ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
  return urlsafe_b64encode(iv + ciphertext).decode('utf-8')

def decryptSecretKey(encrypted):
  key = os.environ.get("AES_SECRET_KEY").encode('utf-8')
  iv = os.environ.get("AES_INITIAL_VECTOR").encode('utf-8')
  encrypted = urlsafe_b64decode(encrypted)
  encrypted = encrypted[16:]
  cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
  decryptor = cipher.decryptor()
  padded_plaintext = decryptor.update(encrypted) + decryptor.finalize()
  unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
  plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
  return plaintext

def generateQrCode(user):
  qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
  )
  secret_key = decryptSecretKey(user['secret_key']).decode('utf-8')
  email = user['email']
  data = f"otpauth://totp/:Amry%20Site?secret={secret_key}&user={email}"
  qr.add_data(data)
  qr.make(fit=True)
  img = qr.make_image(fill_color="black", back_color="white")
  img_buffer = io.BytesIO()
  img.save(img_buffer)
  img_buffer.seek(0)
  return base64.b64encode(img_buffer.read()).decode('utf-8')

def verifyTOTP(totp, encrypted_secret_key):
  secret_key = decryptSecretKey(encrypted_secret_key)
  return totp == getTOTP(secret_key)

@app.route('/')
def landingPage():
  email = verifyLoginToken() 
  if email:
    return redirect(url_for('getDashboard'))
  return redirect(url_for('login'))

@app.route('/register',methods = ['GET','POST'])
def register():
  if request.method == 'GET':
    email = verifyLoginToken() 
    if email:
      return redirect(url_for('getDashboard'))
    return render_template('register.html')
  email = request.form.get('email')
  name = request.form.get('name')
  address = request.form.get('address')
  phone_number = request.form.get('phone_number')
  password = request.form.get('password')
  confirmPassword = request.form.get('confirmPassword')
  if (confirmPassword!=password):
    return '<h3>Password not match</h3>'
  secret_key = secretKeyGenerator()
  user = User(email, name, address, phone_number, hashPassword(password), encryptSecretKey(secret_key))
  if (insertUser(user)):
    resp = make_response(redirect(url_for('getDashboard')))
    resp.set_cookie('token',generateLoginToken(email),info='Registration Success')
    return resp
  else:
    return '<h3>Registration Failed! Email is Used</h3>'

@app.route('/login',methods = ['GET','POST'])
def login():
  if request.method == 'GET':
    email = verifyLoginToken()
    if email:
      return redirect(url_for('getDashboard'))
    return render_template('login.html')
  email = request.form.get('email')
  password = request.form.get('password')
  hashedPassword = hashPassword(password)
  user = getUser(email)
  if not user:
    return "<h3>wrong email</h3>"
  if hashedPassword == (user['password']):
    resp = render_template('totp.html')
    app.secret_key = os.environ.get("APP_SECRET_KEY")
    session['email'] = email
    return resp
  else:
    return "<h3>wrong password</h3>"

@app.route('/dashboard',methods = ['GET','POST'])
def getDashboard():
  email = verifyLoginToken()
  info = request.args.get('info', '')
  if not email:
    return redirect(url_for('login'))
  if request.method == 'GET':
    user = getUser(email) 
    resp = render_template('dashboard.html',info=info, email=user['email'],name=user['name'],address=user['address'],phone_number=user['phone_number'])
    return resp

@app.route('/2fa-setup',methods = ['GET','POST'])
def setTwoFactorAuth():
  email = verifyLoginToken() 
  if not email:
    return redirect(url_for('login'))
  if request.method == 'GET':
    user = getUser(email) 
    qrcode_image = generateQrCode(user)
    return render_template('two-fa.html', qrcode_image=qrcode_image)
  totp = request.form.get('totp')
  user = getUser(email)
  totp_verified = verifyTOTP(totp, user['secret_key'])
  if totp_verified:
    resp = make_response(redirect(url_for('getDashboard', info='Two-Factor Auth Setup Successfully')))
    return resp
  return "failed"

@app.route('/2fa-verify',methods = ['GET','POST'])
def verifyTwoFactorAuth():
  app.secret_key = os.environ.get("APP_SECRET_KEY")
  email = session['email'] 
  if not email:
    return redirect(url_for('login'))
  if request.method == 'GET':
    return render_template('totp.html')
  totp = request.form.get('totp')
  user = getUser(email)
  totp_verified = verifyTOTP(totp, user['secret_key'])
  if totp_verified:
    resp = make_response(redirect(url_for('getDashboard', info='Login Success')))
    resp.set_cookie('token',generateLoginToken(email))
    return resp
  return "<h3>wrong TOTP</h3>"

@app.route('/database')
def getDatabase():
  users = getAllUsers()
  users_list = []
  for user in users:
    users_list.append({
        'email': user.email,
        'name': user.name,
        'address': user.address,
        'phone_number': user.phone_number,
        'password': user.password,
        'secret_key':user.secret_key
    })
  return jsonify(users_list)

@app.route('/logout')
def logout():
  resp = make_response(redirect(url_for('login')))
  resp.set_cookie('token', '',expires=0)
  return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)