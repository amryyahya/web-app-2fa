import sqlite3, os
from user import User
from google.cloud import storage

client = storage.Client.from_service_account_json("sa.json")
bucket_name = 'user-amry-bucket'
source_blob_name = 'users.db'
destination_file_name = 'users.db'

def download_from_gcs():
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

def upload_to_gcs():
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.upload_from_filename(destination_file_name)

users = []
def createTable():
    download_from_gcs()
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, name TEXT, address TEXT, phone_number TEXT, password TEXT, secret_key TEXT)")
    conn.commit()
    conn.close()
    upload_to_gcs()

def insertUser(user):
    download_from_gcs()
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT email FROM users WHERE email=?", (user.email,))
    existing_email = cur.fetchone()
    if existing_email:
      return False
    else:
      cur.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", (
          user.email,
          user.name,
          user.address,
          user.phone_number,
          user.password,
          user.secret_key
      ))
    conn.commit()
    conn.close()
    upload_to_gcs()
    return True

def getUser(email):
    download_from_gcs()
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    conn.commit()
    conn.close()
    if user:
      return user
    else:
      return False

def deleteUser(email):
    download_from_gcs()
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE email=?", (email,))
    conn.commit()
    conn.close()
    upload_to_gcs()
    return True

def getAllUsers():
    download_from_gcs()
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    for row in rows:
      print(row)
    cur.close()
    conn.close()
  