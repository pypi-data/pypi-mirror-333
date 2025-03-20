import pyodbc
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

class Auth:
    _authenticated = False 
    def __init__(self, email: str, password: str):
        PROD_ETMS_DB =  os.getenv("PROD_ETMS_DB")
        self.email = email
        self.password = password.encode("utf-8")  
        self.db_conn_string = PROD_ETMS_DB

    def authenticate(self):
        try:
            conn = pyodbc.connect(self.db_conn_string)
            cursor = conn.cursor()

            query = "SELECT password FROM [ETMS_Production].[dbo].[etms_users] WHERE email = ?"
            cursor.execute(query, (self.email,))
            result = cursor.fetchone()

            if not result:
                return "Failed to authenticate: User not found"

            stored_hashed_password = result[0]

            if isinstance(stored_hashed_password, bytes):
                stored_hashed_password = stored_hashed_password.decode("utf-8")

            if bcrypt.checkpw(self.password, stored_hashed_password.encode("utf-8")):
                Auth._authenticated = True
                conn.close()
                return "Authentication successful"
            else:
                conn.close()
                return "Failed to authenticate: Incorrect password"
            

        except Exception as e:
            return f"Error during authentication: {str(e)}"
