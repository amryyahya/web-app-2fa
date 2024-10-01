# Simple 2FA Login and Register Website

This project is a simple web application built with Python Flask as the backend, which implements a two-factor authentication (2FA) system. The website allows users to register and log in using JWT-based authentication and employs a TOTP (Time-based One-Time Password) system that is secured by the HMAC-Photon algorithm. This project is the output of my S1 thesis.

## Features
- **User Registration**: Create a new account with email and password.
- **User Login**: Authenticate using JWT after providing correct credentials.
- **2FA (Two-Factor Authentication)**: The login process is secured with a TOTP generated by the HMAC-Photon algorithm for additional security.
- **JWT Authentication**: Uses JSON Web Tokens (JWT) for session management.

## Technology Stack
- **Backend**: Python Flask
- **Authentication**: 
  - JWT (JSON Web Tokens) for secure token-based authentication.
  - TOTP with HMAC-Photon for 2FA.
- **Frontend**: Simple HTML/CSS (can be extended as needed).

## Installation
### Method : Using Docker (Make sure [docker-engine](https://docs.docker.com/engine/install/) have been installed on your device)
1. Clone the repository:
   ```bash
   git clone https://github.com/amryyahya/web-app-2fa.git
   cd web-app-2fa
2. Set up environment variables: Edit .env file to store the environment variables:
   ```bash
    AES_INITIAL_VECTOR=16-bytes string
    AES_SECRET_KEY=32-bytes string
    JWT_SECRET_KEY=32-bytes string
    APP_SECRET_KEY=32-bytes string
    QRCODE_KEY=16-bytes string
    QRCODE_IV=16-bytes string
3. Build and run docker container
    ```bash
    docker build -t web-app-2fa .
    docker run -p 5000:5000 web-app-2fa

### Method 2: Install Python Locally (Make sure [python3](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/) have been installed on your device)
1. Clone the repository:
   ```bash
   git clone https://github.com/amryyahya/web-app-2fa.git
   cd web-app-2fa
2. Install dependencies:
   ```bash
    pip install -r requirements.txt
3. Set up environment variables: Edit .env file to store the environment variables:
   ```bash
    AES_INITIAL_VECTOR=16-bytes string
    AES_SECRET_KEY=32-bytes string
    JWT_SECRET_KEY=32-bytes string
    APP_SECRET_KEY=32-bytes string
    QRCODE_KEY=16-bytes string
    QRCODE_IV=16-bytes string
4. Run the application:
   ```bash
   python3 app.py

## Usage
- Register a new account by providing an email, password, and other data dummy (name, phone number, address).
- 2FA must be configured during registration session.
- Log in using the registered credentials. A JWT token will be generated upon successful login.
- Verify the 2FA by entering the TOTP generated by the HMAC-Photon algorithm.

## 2FA Implementation
The Time-based One-Time Password (TOTP) system is secured by the HMAC-Photon algorithm, providing an extra layer of security during the login process.

## License
This project is licensed under the MIT License.

## Acknowledgements
This project was developed as the output of my S1 thesis.
