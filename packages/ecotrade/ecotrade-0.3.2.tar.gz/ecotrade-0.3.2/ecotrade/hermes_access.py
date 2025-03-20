import os
import pyodbc
from dotenv import load_dotenv
from ecotrade.utils import requires_auth
load_dotenv()

@requires_auth
def get_hermes_keys():
    PROD_ETMS_DB =  os.getenv("PROD_ETMS_DB")
    conn = pyodbc.connect(PROD_ETMS_DB)
    cursor = conn.cursor()

    # Example query to get the Hermes keys
    select_query = '''
        SELECT key_admin, key_val 
        FROM key_manager
        WHERE functionality = 'hermes' AND key_admin = 'global.user'
        '''
    cursor.execute(select_query)
    rows = cursor.fetchall()
    
    # Initialize variables
    username = ""
    password = ""
    # Print the results and set username and password
    for row in rows:
        username = row.key_admin
        password = row.key_val
        
        return ({"username": username, "password": password})
    # Close the connection once done
    conn.close()