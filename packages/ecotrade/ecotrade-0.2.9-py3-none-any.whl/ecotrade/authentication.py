import pyodbc
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

class Auth:
    _authenticated = False  # Class-level variable to track authentication status
    def __init__(self, email: str, password: str):
        PROD_ETMS_DB = os.getenv("PROD_ETMS_DB")
        self.email = email
        self.password = password.encode("utf-8")  # Ensure password is in bytes
        self.db_conn_string = PROD_ETMS_DB

    def authenticate(self):
        try:
            conn = pyodbc.connect(self.db_conn_string)
            cursor = conn.cursor()

            # Query to fetch the stored hashed password for the provided email
            query = "SELECT password FROM [ETMS_Production].[dbo].[etms_users] WHERE email = ?"
            cursor.execute(query, (self.email,))
            result = cursor.fetchone()

            if not result:
                return "Failed to authenticate: User not found"

            stored_hashed_password = result[0]

            # Decode if the password is stored as bytes
            if isinstance(stored_hashed_password, bytes):
                stored_hashed_password = stored_hashed_password.decode("utf-8")

            # Compare the stored hashed password with the provided password
            if bcrypt.checkpw(self.password, stored_hashed_password.encode("utf-8")):
                Auth._authenticated = True  # Successfully authenticated
                conn.close()
                return "Authentication successful"
            else:
                conn.close()
                return "Failed to authenticate: Incorrect password"

        except Exception as e:
            return f"Error during authentication: {str(e)}"
