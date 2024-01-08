import hashlib, qrcode, io, os, base64, string, random, jwt, datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def secretKeyGenerator():
  characters = string.ascii_letters + string.digits
  secret_key = ''.join(random.choice(characters) for i in range(32)).encode('utf-8')
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
  return plaintext.decode('utf-8')
