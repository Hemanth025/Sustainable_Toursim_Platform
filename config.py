"""
Configuration file for EcoJourney Authentication System
Update these settings with your MySQL credentials
"""

# MySQL Database Configuration
# TODO: Update these with your actual MySQL credentials
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Hemanth@1105',
    'database': 'ecojourney_db',
    'port': 3306
}

# OTP Configuration
OTP_EXPIRY_MINUTES = 10  # OTP valid for 10 minutes
OTP_LENGTH = 6           # 6-digit OTP

# Session Configuration
REMEMBER_ME_DAYS = 30    # Remember me cookie duration
SESSION_LIFETIME_HOURS = 24  # Session timeout

# Password Requirements
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGIT = True
PASSWORD_REQUIRE_SPECIAL = True

# Database Table Creation SQL
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    otp_code VARCHAR(6),
    otp_expiry DATETIME,
    is_verified BOOLEAN DEFAULT FALSE,
    remember_token VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
