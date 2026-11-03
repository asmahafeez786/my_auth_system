# My Auth System

A backend authentication system built with Python and Flask. It provides user registration, login, JWT-based authentication, protected routes, and email-based password recovery.

## Overview

My Auth System is a REST API-based application designed to handle user authentication and account security.

It uses Flask for backend development, SQLite for database management, and Bcrypt for password hashing. JWT is used to manage authenticated sessions and control access to protected resources.

The application also includes an email-based OTP verification process for password recovery.

## Features

- User registration and login
- Secure password hashing using Bcrypt
- JWT-based authentication
- Protected API endpoints
- Email-based OTP verification
- Password recovery and reset
- Change password functionality
- OTP expiration after 5 minutes
- Hashed OTP storage
- JWT token invalidation using token versioning
- SQLite database integration

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | REST API development |
| Flask-SQLAlchemy | Database operations |
| SQLite | Database management |
| Flask-Bcrypt | Password and OTP hashing |
| Flask-JWT-Extended | JWT authentication |
| Python-dotenv | Environment variable management |
| Gmail SMTP | Email delivery |

## Project Structure

```text
my_auth_system/
│
├── app.py
├── config.py
├── models.py
├── routes.py
├── services.py
├── requirements.txt
├── .gitignore
├── .env
│
└── instance/
    └── site.db
```

**Note:** `.env`, `site.db`, and `.venv` are local files and should not be committed to GitHub.

## Authentication Flow

The application follows this authentication process:

1. A user submits registration details.
2. The password is hashed using Bcrypt.
3. User information is stored in the SQLite database.
4. During login, the submitted credentials are verified.
5. A JWT access token is generated after successful authentication.
6. The token is used to access protected API endpoints.
7. For password recovery, an OTP is generated and sent through email.
8. The OTP is verified before allowing a password reset.

## API Reference

The application provides the following six API endpoints.

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/signup` | Register a new user | Not Required |
| POST | `/login` | Authenticate a user | Not Required |
| GET | `/protected` | Access protected resources | JWT Required |
| POST | `/forgot-password` | Request password recovery OTP | Not Required |
| POST | `/reset-password` | Reset password using OTP | Not Required |
| PUT | `/change-password` | Change existing password | JWT Required |

### 1. User Registration

**Endpoint:** `/signup`

**Method:** POST

Request body:

```json
{
    "name": "John",
    "email": "john@example.com",
    "password": "your_password"
}
```

The application validates the required fields, checks whether the email already exists, hashes the password, and stores the new user.

### 2. User Login

**Endpoint:** `/login`

**Method:** POST

Request body:

```json
{
    "email": "john@example.com",
    "password": "your_password"
}
```

After successful authentication, the server generates a JWT access token.

### 3. Protected Route

**Endpoint:** `/protected`

**Method:** GET

Requires a valid JWT access token.

The endpoint verifies the authenticated user and returns their name and email.

### 4. Forgot Password

**Endpoint:** `/forgot-password`

**Method:** POST

Request body:

```json
{
    "email": "john@example.com"
}
```

A six-digit OTP is generated and sent to the registered email address.

The OTP is stored as a Bcrypt hash and expires after five minutes.

### 5. Reset Password

**Endpoint:** `/reset-password`

**Method:** POST

Request body:

```json
{
    "email": "john@example.com",
    "otp": "123456",
    "new_password": "new_password"
}
```

The application verifies the OTP and its expiration before updating the password.

After a successful reset, the OTP is cleared and previously issued JWT tokens are invalidated through token versioning.

### 6. Change Password

**Endpoint:** `/change-password`

**Method:** PUT

Requires a valid JWT access token.

Request body:

```json
{
    "old_password": "current_password",
    "new_password": "new_password"
}
```

The application verifies the old password before updating it.

A new access token is generated after a successful password change.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/asmahafeez786/my_auth_system.git
```

### 2. Navigate to the Project Directory

```bash
cd my_auth_system
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root directory.

Configure the required environment variables:

```env
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
```

Replace the placeholder values with your actual configuration.

Keep your environment variables private. Never upload your `.env` file or expose your email credentials and secret keys.

## Running the Application

Start the Flask application:

```bash
python app.py
```

The local development server will be available at:

```text
http://127.0.0.1:5000
```

## API Testing

The application can be tested using Postman.

For protected endpoints, include the JWT access token in the request header:

```http
Authorization: Bearer <access_token>
```

Test the registration, login, protected route, password recovery, password reset, and password change workflows.

## Security Implementation

The project implements several security measures:

- Bcrypt hashing for user passwords.
- Hashed OTP storage.
- Five-minute OTP expiration.
- JWT-based authentication.
- Protected API endpoints.
- Token expiration.
- Token versioning for session invalidation.
- Environment variables for sensitive configuration.

## Developer

**Asma Hafeez**

Python | Flask | Backend Development