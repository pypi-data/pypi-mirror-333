import pyodbc

def get_hermes_keys():
    try:
        # Connect to the database
        connection = pyodbc.connect(
            r'DRIVER={SQL Server};'
            r'SERVER=192.168.5.35\SQLEXPRESS;'
            r'DATABASE=ETMS_Production;'
            r'UID=deal;'
            r'PWD=deal2023!'
        )
        cursor = connection.cursor()
        
        # Query to select key_admin and key_val where functionality is "hermes" and key_admin is "global.user"
        select_query = '''
        SELECT key_admin, key_val 
        FROM key_manager
        WHERE functionality = 'hermes' AND key_admin = 'global.user'
        '''
        
        # Execute the query
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

    except pyodbc.Error as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Close the connection
        if connection:
            connection.close()