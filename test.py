import hashlib, qrcode, io, os, base64, string, random, jwt, datetime
from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for, send_file, session
from user import User
from totp import getTOTP
from user_management import createTable, insertUser, getAllUsers, getUser
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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
  print(plaintext)
  return plaintext

user = getUser('amry@yahya.com')

print(decryptSecretKey(user['secret_key']))