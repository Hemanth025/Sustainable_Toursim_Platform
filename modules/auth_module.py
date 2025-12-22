"""
Authentication Module for EcoJourney
Handles user registration, login, OTP verification, and session management
"""

import random
import string
import re
from datetime import datetime, timedelta
from functools import wraps
from flask import session, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash

# Import configuration
try:
    from config import (
        MYSQL_CONFIG, 
        OTP_EXPIRY_MINUTES, 
        OTP_LENGTH,
        PASSWORD_MIN_LENGTH,
        PASSWORD_REQUIRE_UPPERCASE,
        PASSWORD_REQUIRE_LOWERCASE,
        PASSWORD_REQUIRE_DIGIT,
        PASSWORD_REQUIRE_SPECIAL,
        CREATE_USERS_TABLE
    )
except ImportError:
    # Default values if config not found
    MYSQL_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'ecojourney_db',
        'port': 3306
    }
    OTP_EXPIRY_MINUTES = 10
    OTP_LENGTH = 6
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_DIGIT = True
    PASSWORD_REQUIRE_SPECIAL = True
    CREATE_USERS_TABLE = ""

# Try to import MySQL connector
try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False


# ==================== DATABASE CONNECTION ====================

def get_db_connection():
    """Create and return a MySQL database connection"""
    if not MYSQL_AVAILABLE:
        print("Warning: mysql-connector-python not installed. Run: pip install mysql-connector-python")
        return None
    
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None
    return None


def init_database():
    """Initialize the database with required tables"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_USERS_TABLE)
        connection.commit()
        print("Database tables initialized successfully")
        return True
    except Error as e:
        print(f"Database initialization error: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# ==================== PASSWORD UTILITIES ====================

def validate_password_strength(password):
    """
    Validate password meets strength requirements
    Returns: (is_valid: bool, errors: list, strength_score: int 0-100)
    """
    errors = []
    score = 0
    
    if len(password) < PASSWORD_MIN_LENGTH:
        errors.append(f"Password must be at least {PASSWORD_MIN_LENGTH} characters")
    else:
        score += 20
    
    if PASSWORD_REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    else:
        score += 20
    
    if PASSWORD_REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    else:
        score += 20
    
    if PASSWORD_REQUIRE_DIGIT and not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    else:
        score += 20
    
    if PASSWORD_REQUIRE_SPECIAL and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character (!@#$%^&*)")
    else:
        score += 20
    
    # Bonus points for length
    if len(password) >= 12:
        score = min(100, score + 10)
    
    return (len(errors) == 0, errors, score)


def hash_password(password):
    """Generate a secure hash of the password"""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)


def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return check_password_hash(password_hash, password)


# ==================== OTP UTILITIES ====================

def generate_otp():
    """Generate a random 6-digit OTP code"""
    return ''.join(random.choices(string.digits, k=OTP_LENGTH))


def get_otp_expiry():
    """Get OTP expiry datetime"""
    return datetime.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)


def is_otp_valid(stored_otp, stored_expiry, provided_otp):
    """Check if OTP is valid and not expired"""
    if not stored_otp or not stored_expiry:
        return False
    
    if datetime.now() > stored_expiry:
        return False
    
    return stored_otp == provided_otp


# ==================== USER OPERATIONS ====================

def create_user(first_name, last_name, username, email, phone, password):
    """
    Create a new user in the database
    Returns: (success: bool, message: str, user_id: int or None)
    """
    connection = get_db_connection()
    if not connection:
        return (False, "Database connection failed", None)
    
    try:
        cursor = connection.cursor()
        
        # Hash the password
        password_hash = hash_password(password)
        
        # Generate OTP for verification
        otp = generate_otp()
        otp_expiry = get_otp_expiry()
        
        # Insert user
        query = """
        INSERT INTO users (first_name, last_name, username, email, phone, password_hash, otp_code, otp_expiry)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (first_name, last_name, username, email, phone, password_hash, otp, otp_expiry)
        
        cursor.execute(query, values)
        connection.commit()
        
        user_id = cursor.lastrowid
        return (True, otp, user_id)  # Return OTP for display (simulated)
        
    except Error as e:
        error_msg = str(e)
        if "Duplicate entry" in error_msg:
            if "username" in error_msg:
                return (False, "Username already exists", None)
            elif "email" in error_msg:
                return (False, "Email already registered", None)
            elif "phone" in error_msg:
                return (False, "Phone number already registered", None)
        return (False, f"Registration failed: {error_msg}", None)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def verify_user_otp(identifier, otp):
    """
    Verify OTP and mark user as verified
    identifier can be email or username
    Returns: (success: bool, message: str)
    """
    connection = get_db_connection()
    if not connection:
        return (False, "Database connection failed")
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Find user by email or username
        query = """
        SELECT id, otp_code, otp_expiry, is_verified 
        FROM users 
        WHERE email = %s OR username = %s
        """
        cursor.execute(query, (identifier, identifier))
        user = cursor.fetchone()
        
        if not user:
            return (False, "User not found")
        
        if user['is_verified']:
            return (True, "Already verified")
        
        # Check OTP
        if not is_otp_valid(user['otp_code'], user['otp_expiry'], otp):
            return (False, "Invalid or expired OTP")
        
        # Mark as verified and clear OTP
        update_query = """
        UPDATE users 
        SET is_verified = TRUE, otp_code = NULL, otp_expiry = NULL 
        WHERE id = %s
        """
        cursor.execute(update_query, (user['id'],))
        connection.commit()
        
        return (True, "Account verified successfully")
        
    except Error as e:
        return (False, f"Verification failed: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def authenticate_user(identifier, password):
    """
    Authenticate user credentials
    Returns: (success: bool, message: str, user_data: dict or None, otp: str or None)
    """
    connection = get_db_connection()
    if not connection:
        return (False, "Database connection failed", None, None)
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Find user by email or username
        query = """
        SELECT id, first_name, last_name, username, email, phone, password_hash, is_verified 
        FROM users 
        WHERE (email = %s OR username = %s)
        """
        cursor.execute(query, (identifier, identifier))
        user = cursor.fetchone()
        
        if not user:
            return (False, "Invalid credentials", None, None)
        
        if not verify_password(password, user['password_hash']):
            return (False, "Invalid credentials", None, None)
        
        if not user['is_verified']:
            return (False, "Account not verified. Please verify your email first.", None, None)
        
        # Generate OTP for MFA
        otp = generate_otp()
        otp_expiry = get_otp_expiry()
        
        # Store OTP
        update_query = "UPDATE users SET otp_code = %s, otp_expiry = %s WHERE id = %s"
        cursor.execute(update_query, (otp, otp_expiry, user['id']))
        connection.commit()
        
        # Remove sensitive data
        del user['password_hash']
        
        return (True, "Credentials valid. OTP sent.", user, otp)
        
    except Error as e:
        return (False, f"Authentication failed: {e}", None, None)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def verify_login_otp(user_id, otp):
    """Verify MFA OTP for login"""
    connection = get_db_connection()
    if not connection:
        return (False, "Database connection failed")
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT otp_code, otp_expiry FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return (False, "User not found")
        
        if not is_otp_valid(user['otp_code'], user['otp_expiry'], otp):
            return (False, "Invalid or expired OTP")
        
        # Clear OTP after successful verification
        update_query = "UPDATE users SET otp_code = NULL, otp_expiry = NULL WHERE id = %s"
        cursor.execute(update_query, (user_id,))
        connection.commit()
        
        return (True, "Login successful")
        
    except Error as e:
        return (False, f"Verification failed: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def request_password_reset(identifier):
    """
    Request password reset OTP
    Returns: (success: bool, message: str, otp: str or None)
    """
    connection = get_db_connection()
    if not connection:
        return (False, "Database connection failed", None)
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT id, email FROM users WHERE email = %s OR username = %s"
        cursor.execute(query, (identifier, identifier))
        user = cursor.fetchone()
        
        if not user:
            return (False, "Account not found", None)
        
        # Generate OTP
        otp = generate_otp()
        otp_expiry = get_otp_expiry()
        
        update_query = "UPDATE users SET otp_code = %s, otp_expiry = %s WHERE id = %s"
        cursor.execute(update_query, (otp, otp_expiry, user['id']))
        connection.commit()
        
        return (True, "OTP generated for password reset", otp)
        
    except Error as e:
        return (False, f"Request failed: {e}", None)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def reset_password(identifier, otp, new_password):
    """
    Reset password with OTP verification
    Returns: (success: bool, message: str)
    """
    connection = get_db_connection()
    if not connection:
        return (False, "Database connection failed")
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT id, otp_code, otp_expiry FROM users WHERE email = %s OR username = %s"
        cursor.execute(query, (identifier, identifier))
        user = cursor.fetchone()
        
        if not user:
            return (False, "Account not found")
        
        if not is_otp_valid(user['otp_code'], user['otp_expiry'], otp):
            return (False, "Invalid or expired OTP")
        
        # Validate new password
        is_valid, errors, _ = validate_password_strength(new_password)
        if not is_valid:
            return (False, errors[0])
        
        # Update password
        new_hash = hash_password(new_password)
        update_query = """
        UPDATE users 
        SET password_hash = %s, otp_code = NULL, otp_expiry = NULL 
        WHERE id = %s
        """
        cursor.execute(update_query, (new_hash, user['id']))
        connection.commit()
        
        return (True, "Password reset successfully")
        
    except Error as e:
        return (False, f"Reset failed: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def check_unique(field, value):
    """
    Check if a field value is unique in the database
    Returns: (is_unique: bool, message: str)
    """
    connection = get_db_connection()
    if not connection:
        return (True, "Cannot verify - database unavailable")  # Allow in case of DB issues
    
    try:
        cursor = connection.cursor()
        
        if field not in ['username', 'email', 'phone']:
            return (False, "Invalid field")
        
        query = f"SELECT COUNT(*) FROM users WHERE {field} = %s"
        cursor.execute(query, (value,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            return (False, f"{field.capitalize()} already exists")
        return (True, f"{field.capitalize()} is available")
        
    except Error as e:
        return (True, "Cannot verify uniqueness")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def resend_otp(identifier):
    """
    Resend OTP to user
    Returns: (success: bool, message: str, otp: str or None)
    """
    connection = get_db_connection()
    if not connection:
        return (False, "Database connection failed", None)
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT id FROM users WHERE email = %s OR username = %s"
        cursor.execute(query, (identifier, identifier))
        user = cursor.fetchone()
        
        if not user:
            return (False, "Account not found", None)
        
        otp = generate_otp()
        otp_expiry = get_otp_expiry()
        
        update_query = "UPDATE users SET otp_code = %s, otp_expiry = %s WHERE id = %s"
        cursor.execute(update_query, (otp, otp_expiry, user['id']))
        connection.commit()
        
        return (True, "OTP resent", otp)
        
    except Error as e:
        return (False, f"Failed to resend OTP: {e}", None)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def set_remember_token(user_id, token):
    """Store remember me token for user"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "UPDATE users SET remember_token = %s WHERE id = %s"
        cursor.execute(query, (token, user_id))
        connection.commit()
        return True
    except Error:
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_user_by_remember_token(token):
    """Get user by remember me token"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT id, first_name, last_name, username, email 
        FROM users 
        WHERE remember_token = %s AND is_verified = TRUE
        """
        cursor.execute(query, (token,))
        return cursor.fetchone()
    except Error:
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def clear_remember_token(user_id):
    """Clear remember me token on logout"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "UPDATE users SET remember_token = NULL WHERE id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()
        return True
    except Error:
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# ==================== FLASK DECORATORS ====================

def login_required(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('welcome'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """Get current logged-in user from session"""
    if 'user_id' in session:
        return {
            'id': session.get('user_id'),
            'username': session.get('username'),
            'email': session.get('email'),
            'first_name': session.get('first_name'),
            'last_name': session.get('last_name')
        }
    return None
