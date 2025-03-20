import pyodbc
from flask import g, request

connection_prod = (
    r"DRIVER={SQL Server};"
    r"SERVER=192.168.5.35\SQLEXPRESS;"
    r"DATABASE=ETMS_Production;"
    r"UID=deal;"
    r"PWD=deal2023!"
)

connection_deal = (
    r"DRIVER={SQL Server};"
    r"SERVER=192.168.5.35\SQLEXPRESS;"
    r"DATABASE=deal;"
    r"UID=deal;"
    r"PWD=deal2023!"
)

connection_pow = (
    r"DRIVER={SQL Server};"
    r"SERVER=192.168.5.35\SQLEXPRESS;"
    r"DATABASE=POW;"
    r"UID=deal;"
    r"PWD=deal2023!"
)

connection_pico = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=picosys.westeurope.cloudapp.azure.com,1437;"
    r"DATABASE=USER_ECOTRADE;"
    r"UID=ecotrade;"
    r"PWD=v5V4sZGjFjuw3saqJIuO"
)


def get_connection_string_db(type):
    """
    Retrieves the connection string for the specified database type.

    Parameters:
        - type (str): The type of database connection to retrieve. 
                      Acceptable values are:
                      - "PICO" for the Pico database connection.
                      - "PROD" for the production database connection.
                      - "DEAL" for the test database connection.

    Returns:
        - str: The connection string for the specified database type.

    Example usage:
        - To get the connection string for the Pico database:
          connection = get_connection_string_db("PICO")

        - To get the connection string for the Production database:
          connection = get_connection_string_db("PROD")
          
        - To get the connection string for the DEAL database:
          connection = get_connection_string_db("DEAL")
        
        - To get the connection string for the POW database:
          connection = get_connection_string_db("POW")

    Note:
        - Ensure the connection variables (e.g., `connection_pico`, `connection_prod`, `connection_deal`, `connection_pow`) 
          are properly defined and accessible in the script before calling this function.
    """
    
    if type == "PICO":
        connection = connection_pico
    elif type == "PROD":
        connection = connection_prod
    elif type == "DEAL":
        connection = connection_deal
    elif type == "POW":
        connection = connection_pow
    
    return connection
