import os
from dotenv import load_dotenv
from ecotrade.utils import requires_auth

# Load environment variables from .env file
load_dotenv()

@requires_auth
def get_connection_string_db(db_type):
    """
    Retrieves the connection string for the specified database type.

    Parameters:
        - type (str): The type of database connection to retrieve. 
                      Acceptable values are:
                      - "DEAL" for the test database connection.
                      - "POW" for the power database connection.
                      - "PICO" for the PicoSystem database connection.
                      - "PROD_ETMS" for the ETMS production database connection.

    Returns:
        - str: The connection string for the specified database type.

    Example usage:
        - To get the connection string for the DEAL database:
          connection = get_connection_string_db("DEAL")
        
        - To get the connection string for the POW database:
          connection = get_connection_string_db("POW")
          
        - To get the connection string for the Pico database:
          connection = get_connection_string_db("PICO")

        - To get the connection string for the ETMS Production database:
          connection = get_connection_string_db("PROD_ETMS")
          
    Note:
        - Ensure the connection variables (e.g., `connection_pico`, `connection_prod_etms`, `connection_deal`, `connection_pow`) 
          are properly defined and accessible in the script before calling this function.
    """
    
    db_connections = {
        "PICO": os.getenv("PICO_DB"),
        "PROD_ETMS": os.getenv("PROD_ETMS_DB"),
        "DEAL": os.getenv("DEAL_DB"),
        "POW": os.getenv("POW_DB"),
    }

    connection = db_connections.get(db_type)
    if connection is None:
        raise ValueError(f"Invalid database type: {db_type}")
    return connection