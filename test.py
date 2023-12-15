import qrcode
# import os
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import padding
# from base64 import urlsafe_b64encode, urlsafe_b64decode
# from os.path import join, dirname
# from dotenv import load_dotenv
# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)
# aes_key = os.environ.get("SECRET_KEY").encode('utf-8')
# aes_init_vector = os.environ.get("INITIAL_VECTOR").encode('utf-8')

# # Encrypt function
# def encrypt(plaintext, key):
#     # Generate a random initialization vector (IV)
#     iv = aes_init_vector

#     # Pad the plaintext to be a multiple of the block size
#     padder = padding.PKCS7(algorithms.AES.block_size).padder()
#     padded_plaintext = padder.update(plaintext) + padder.finalize()

#     # Create an AES cipher object with CBC mode
#     cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

#     # Encrypt the plaintext
#     encryptor = cipher.encryptor()
#     ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

#     # Combine IV and ciphertext and return the result
#     return urlsafe_b64encode(iv + ciphertext)

# # Decrypt function
# def decrypt(ciphertext, key):
#     # Decode the base64-encoded ciphertext
#     ciphertext = urlsafe_b64decode(ciphertext)

#     # Extract the IV from the ciphertext
#     iv = ciphertext[:16]
#     ciphertext = ciphertext[16:]

#     # Create an AES cipher object with CBC mode
#     cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

#     # Decrypt the ciphertext
#     decryptor = cipher.decryptor()
#     padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

#     # Unpad the plaintext
#     unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
#     plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

#     return plaintext.decode('utf-8')

# # Example usage
# key = aes_key
# plaintext = "Hello, AES!"

# # Encrypt the plaintext
# encrypted_text = encrypt(plaintext.encode('utf-8'), key)
# h=encrypted_text.decode('utf-8')
# print(f'Encrypted Text: {h}')

# # Decrypt the ciphertext
# decrypted_text = decrypt(encrypted_text, key)
# print(f'Decrypted Text: {decrypted_text}')


# import sqlite3

# def show_db_contents(db_file):
#     # Connect to SQLite database
#     conn = sqlite3.connect(db_file)

#     # Create a cursor object to interact with the database
#     cursor = conn.cursor()

#     # Execute a query to fetch all tables in the database
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = cursor.fetchall()

#     # Display tables
#     for table in tables:
#         table_name = table[0]
#         print(f"Table: {table_name}")

#         # Execute a query to fetch all rows from the table
#         cursor.execute(f"SELECT * FROM {table_name};")
#         rows = cursor.fetchall()

#         # Display rows
#         for row in rows:
#             print(row)

#         print("\n")

#     # Close the connection
#     conn.close()

# # Replace 'example.db' with the name of your SQLite database file
# show_db_contents('users.db')

# import os
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import padding
# from base64 import urlsafe_b64encode, urlsafe_b64decode

# def encrypt(plaintext, key):
#     iv = os.urandom(16)
#     padder = padding.PKCS7(algorithms.AES.block_size).padder()
#     padded_plaintext = padder.update(plaintext) + padder.finalize()
#     cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
#     encryptor = cipher.encryptor()
#     ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
#     return urlsafe_b64encode(iv + ciphertext)

# def decrypt(ciphertext, key):
#     ciphertext = urlsafe_b64decode(ciphertext)
#     iv = ciphertext[:16]
#     ciphertext = ciphertext[16:]
#     cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
#     decryptor = cipher.decryptor()
#     padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
#     unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
#     plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
#     return plaintext.decode('utf-8')

# key = os.urandom(32)
# plaintext = "Hello, AES!"

# encrypted_text = encrypt(plaintext.encode('utf-8'), key).decode('utf-8')
# print(f'Encrypted Text: {encrypted_text}')

# decrypted_text = decrypt(encrypted_text, key)
# print(f'Decrypted Text: {decrypted_text}')

