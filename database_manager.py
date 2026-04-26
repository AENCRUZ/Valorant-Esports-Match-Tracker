import mysql.connector
from mysql.connector import Error


import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': 'ValorantEsportsTracker'
}
# -----------------------------

class DatabaseManager:
    """
    Handles all database connectivity and operations (CRUD) for the VEMT application.
    Uses the mysql.connector library.
    """

    def __init__(self):
        """Initializes the Database Manager but does not connect immediately."""
        self.connection = None
        self.is_connected = False
        print("Database Manager initialized.")


    def connect(self):
        """Attempts to establish a connection to the MySQL database."""
        if self.connection and self.connection.is_connected():
            print("Already connected to the database.")
            self.is_connected = True
            return True

        print(f"Attempting to connect to database: {DB_CONFIG['database']}...")
        try:
            # Attempt to connect using the configured details
            self.connection = mysql.connector.connect(**DB_CONFIG)

            if self.connection.is_connected():
                cursor = self.connection.cursor()
                # Check server version just to confirm a successful connection
                print(f"Successfully connected to MySQL Server version: {self.connection.get_server_info()}")
                cursor.close()
                self.is_connected = True
                return True
            else:
                print("Connection failed: Could not establish a connection.")
                self.is_connected = False
                return False

        except Error as e:
            
            self.is_connected = False
            print("--- DATABASE CONNECTION ERROR ---")
            print(f"MySQL Error Code: {e.errno}")
            print(f"MySQL Error Message: {e.msg}")

            if e.errno == 2003: 
                 print("ACTION REQUIRED: Check if MySQL server is running on localhost.")
            elif e.errno == 1045: 
                print("ACTION REQUIRED: The 'user' or 'password' in DB_CONFIG is INCORRECT or the user lacks permissions.")
                print(f"Check credentials for user '{DB_CONFIG['user']}' against database '{DB_CONFIG['database']}'.")
            elif e.errno == 1049: 
                 print(f"ACTION REQUIRED: Database '{DB_CONFIG['database']}' does not exist. Create it or correct the name in DB_CONFIG.")
            else:
                print("A general database error occurred.")
            print("---------------------------------")

            return False

    def close(self):
        """Closes the database connection if it is open."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.is_connected = False
            print("Database connection closed.")

    

    def fetch_teams(self):
        """Reads all records from the 'team' table."""
        if not self.connect():
            return []

        cursor = self.connection.cursor(dictionary=True)
        try:
          
            sql = "SELECT team_id, team_name, coach_name FROM team"
            cursor.execute(sql)
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Error reading data: {e}")
            return []
        finally:
            cursor.close()


if __name__ == '__main__':
    db_manager = DatabaseManager()

    # Test the connection
    if db_manager.connect():
        print("\nConnection Test Successful! Now you can use CRUD methods.")
        
       
        teams = db_manager.fetch_teams()
        if teams:
            print("\nFetched Teams:")
            for team in teams:
                print(f"- {team['team_id']}: {team['team_name']} (Coach: {team['coach_name']})")
        else:
             print("\nNo teams found or error during fetch.")

    else:
        print("\nConnection Test Failed. Please fix the configuration in DB_CONFIG.")

    db_manager.close()
