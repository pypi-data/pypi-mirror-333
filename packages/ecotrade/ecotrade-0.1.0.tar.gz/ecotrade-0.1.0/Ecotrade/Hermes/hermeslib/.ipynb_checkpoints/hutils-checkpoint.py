import sys

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
