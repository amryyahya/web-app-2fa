class User:
  def __init__(self, email, name, address, phone_number, password, secret_key=None):
    self.email = email
    self.name = name
    self.address = address
    self.phone_number = phone_number
    self.password = password
    self.secret_key = secret_key