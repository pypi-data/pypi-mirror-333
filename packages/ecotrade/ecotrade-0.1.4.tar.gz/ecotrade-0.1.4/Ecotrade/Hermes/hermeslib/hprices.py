import requests
import sys
import json
from datetime import datetime, timedelta, date
import pandas as pd

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




class Prices:
    
    def __init__(self, session):
        self.session = session
        self.url = f'{base_url}/market/prices'
        self.prices = None

    def get_prices(self, zone, startdate, stopdate, interval = '1H'):
        """
        Retrieves prices for a specific zone within a specified time range.
        Parameters:
            zone (str): The name of the zone for which the prices are desired.
            startdate (datetime): The start time of the time range.
            stopdate (datetime): The stop time of the time range.
            interval (str): The time interval of the prices.
        Returns:
            DataFrame: The prices in a pandas DataFrame format if the request is successful, 
            otherwise returns None.
        """
        
        startdate =  formatting_date(startdate)
        stopdate = formatting_date(stopdate)
                                   
        delta = timedelta(days=1)
        startdate = startdate - delta
        stopdate = stopdate - delta
        payload = {
            "from": startdate.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "to": stopdate.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "zone": zone
        }

        response = self.session.request('get', self.url, payload)
        
        check_status(response)
        
        
        json_response = response.json()
        data = json_response['data']   
        self.prices = pd.DataFrame(data[::-1])         
        self.prices['date'] = pd.to_datetime(self.prices['date']) + pd.Timedelta(days=1)
        self.prices.reset_index(drop=True, inplace=True)      

        if interval == "1H":
            return self.prices
        else:
            df_date = self.prices['date']   
            self.prices = self.prices.select_dtypes(include=['int', 'float']) 
            self.prices = pd.concat([df_date, self.prices], axis=1)  
            self.prices = self.prices.resample(interval, on='date').mean()
            self.prices.reset_index(drop=False, inplace=True)                                
            return self.prices
        
       
        
