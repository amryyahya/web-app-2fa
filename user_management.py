import sqlite3
import random
import os 
import string
from user import User
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
aes_key = os.environ.get("SECRET_KEY").encode('utf-8')
aes_iv = os.environ.get("INITIAL_VECTOR").encode('utf-8')

users = []
def createTable():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, name TEXT, address TEXT, phone_number TEXT, password TEXT, secret_key TEXT)")
    conn.commit()
    conn.close()

def insertUser(user):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT email FROM users WHERE email=?", (user.email,))
    existing_email = cur.fetchone()
    if existing_email:
      return False
    else:
      characters = string.ascii_letters + string.digits
      secret_key = ''.join(random.choice(characters) for i in range(16)).encode('utf-8')
      padder = padding.PKCS7(algorithms.AES.block_size).padder()
      padded_plaintext = padder.update(secret_key) + padder.finalize()
      cipher = Cipher(algorithms.AES(aes_key), modes.CFB(aes_iv), backend=default_backend())
      encryptor = cipher.encryptor()
      ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
      encrypted_secret_key_bytes = urlsafe_b64encode(aes_iv + ciphertext)
      encrypted_secret_key = encrypted_secret_key_bytes.decode('utf-8')
      cur.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", (
          user.email,
          user.name,
          user.address,
          user.phone_number,
          user.password,
          encrypted_secret_key
      ))
    conn.commit()
    conn.close()
    return True

def editUser(user):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE email=?", (user.email,))
    conn.commit()
    conn.close()
    insertUser(user)
    return True

def getUser(email):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    conn.commit()
    conn.close()
    if user:
      return user
    else:
      return False

def getAllUsers():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    users = []
    for i in rows:
        user = User(i[0],i[1], i[2],i[3],i[4],i[5])
        users.append(user)
    conn.close()
    return users