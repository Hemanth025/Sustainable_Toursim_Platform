"""
Database Setup Script for EcoJourney
Run this script to create the database and users table
"""

import mysql.connector
from mysql.connector import Error

# Database credentials (without database name for initial connection)
SETUP_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password',
    'port': 3306
}

# Create users table SQL
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

# Create user history table SQL
CREATE_HISTORY_TABLE = """
CREATE TABLE IF NOT EXISTS user_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    destination_id VARCHAR(50) NOT NULL,
    destination_name VARCHAR(100) NOT NULL,
    search_type VARCHAR(20) DEFAULT 'view',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_history (user_id),
    INDEX idx_destination (destination_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

def setup_database():
    """Create database and users table"""
    connection = None
    cursor = None
    try:
        # Connect to MySQL server (without specifying database)
        print("Connecting to MySQL server...")
        connection = mysql.connector.connect(**SETUP_CONFIG)
        
        if connection.is_connected():
            print("[OK] Connected to MySQL server")
            cursor = connection.cursor()
            
            # Create database
            print("Creating database 'ecojourney_db'...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS ecojourney_db")
            print("[OK] Database created/verified")
            
            # Switch to the database
            cursor.execute("USE ecojourney_db")
            
            # Create users table
            print("Creating 'users' table...")
            cursor.execute(CREATE_USERS_TABLE)
            connection.commit()
            print("[OK] Users table created/verified")
            
            # Create user history table
            print("Creating 'user_history' table...")
            cursor.execute(CREATE_HISTORY_TABLE)
            connection.commit()
            print("[OK] User history table created/verified")
            
            print("")
            print("=" * 50)
            print("[OK] DATABASE SETUP COMPLETE!")
            print("=" * 50)
            print("")
            print("You can now run the application with: python app.py")
            
    except Error as e:
        print("")
        print("[ERROR] " + str(e))
        print("")
        print("Troubleshooting:")
        print("1. Make sure MySQL server is running")
        print("2. Verify your credentials in this file")
        print("3. Check if MySQL is installed correctly")
        
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("")
            print("MySQL connection closed.")

if __name__ == '__main__':
    setup_database()

