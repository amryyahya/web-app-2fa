import hashlib, qrcode, io, os, base64, string, random, datetime, ctypes,jwt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
from os.path import join, dirname
from dotenv import load_dotenv
import jpype

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
jpype.startJVM(classpath=['.'])

def getTOTP(secret_key):
    # lib = ctypes.CDLL('./totp-hmac-photon.so')
    # lib.getTOTP.restype = ctypes.c_int
    # lib.getTOTP.argtypes = [ctypes.c_char_p]
    # totp = lib.getTOTP(secret_key)
    # return str(totp).zfill(6)
    TOTPGenerator = jpype.JClass('TOTP')
    totp = TOTPGenerator.TOTP(secret_key)
    return totp;
    
def getTOTP(secret_key):
    lib = ctypes.CDLL('./totp-hmac-photon.so')
    lib.getTOTP.restype = ctypes.c_int
    lib.getTOTP.argtypes = [ctypes.c_char_p]
    totp = lib.getTOTP(secret_key)
    return str(totp).zfill(6)

def generateLoginToken(email):
  expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=3)
  payload = {
    "email": email,
    "exp": expiration_time
  }
  secret_key = os.environ.get("JWT_SECRET_KEY")
  return jwt.encode(payload, secret_key, algorithm="HS256")

def verifyLoginToken(token):
  if token is None:
    return False
  try:
    secret_key = os.environ.get("JWT_SECRET_KEY")
    decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    email = decoded_payload['email']
    return email
  except Exception as e:
    return False

def hashPassword(password):
  sha256_hash = hashlib.sha256()
  sha256_hash.update(password.encode('utf-8'))
  hashedPassword = sha256_hash.hexdigest()
  return hashedPassword

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
  return plaintext

def generateQrCode(user):
  qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
  )
  secret_key = decryptSecretKey(user['secret_key'])
  email = user['email']
  data = f"otpauth://totp/:Amry%20Site?secret={secret_key.decode('utf-8')}&user={email}"
  qr.add_data(data)
  qr.make(fit=True)
  img = qr.make_image(fill_color="black", back_color="white")
  img_buffer = io.BytesIO()
  img.save(img_buffer)
  img_buffer.seek(0)
  return base64.b64encode(img_buffer.read()).decode('utf-8')
