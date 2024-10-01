import sqlite3
from user import User

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
    return True

def getUser(email):
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
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE email=?", (email,))
    conn.commit()
    conn.close()
    return True

def getAllUsers():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    for row in rows:
      print(row)
    cur.close()
    conn.close()