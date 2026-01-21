"""
User Module for EcoJourney
Handles user-related operations like history tracking and profile management.
"""

from modules.auth_module import get_db_connection
from mysql.connector import Error

def add_user_history(user_id, destination_name, destination_id, search_type='view'):
    """
    Add a record to user's search/view history.
    """
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Insert history record
        query = """
        INSERT INTO user_history (user_id, destination_name, destination_id, search_type)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, destination_name, destination_id, search_type))
        connection.commit()
        return True
        
    except Error as e:
        print(f"Failed to add history: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_user_history(user_id, limit=5):
    """
    Retrieve user's recent history.
    """
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get recent unique history (group by destination to avoid duplicates in list)
        # Note: GROUP BY might pick arbitrary timestamps, so better to use MAX(timestamp)
        query = """
        SELECT destination_name, destination_id, MAX(timestamp) as last_visited
        FROM user_history
        WHERE user_id = %s
        GROUP BY destination_name, destination_id
        ORDER BY last_visited DESC
        LIMIT %s
        """
        cursor.execute(query, (user_id, limit))
        return cursor.fetchall()
        
    except Error as e:
        print(f"Failed to get history: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
