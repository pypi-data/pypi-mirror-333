
import requests
import sys
import json

def check_status(response):
    """
    Check the status of the API. 
    If the status code is not 200, raise an exception.
    """
    if response.status_code != 200:
        print("Error")
        if response.status_code == 400:
            json_response = response.json()
            print("Error message: {}".format(json_response['message']))
        sys.exit(1)
        
    
def formatting_date(date):
    """
    Format the given date by setting the hour to 23:00:00. 
    If the month is between April and October, set the hour to 22:00:00. 
    Return the formatted date.
    """
    
    date = date.replace(hour=23, minute=0, second=0)
    if date.month >= 4 and date.month <= 10:
        date = date.replace(hour=22, minute=0, second=0)

    return date

base_url = "https://hermes.phinergy.biz/api"

def HermesAutentication(username, password):
    """
    Authenticates the user with the given username and password.
    Args:
        username (str): The username for authentication.
        password (str): The password for authentication.
    Returns:
        requests.Session: A session object authenticated with the provided credentials.
    """
    
    session = requests.Session()
    session.timeout = 10

    response   =   session.post(base_url + '/login', json={
        'username' : username,
        'password' : password,
    })

    check_status(response)

    json_response = response.json()
    user          = json_response['user']
    token         = json_response['token']
    print("--- Logged in Hermes! Username: {}".format(user['username']))
    print()

    session.headers['Authorization']   =   'Bearer ' + token # add token to headers of subsequent requests to authenticate them
    
    return session
