import requests
import sys
import json
from hermeslib import hutils
from datetime import datetime, timedelta, date
import pandas as pd

base_url = "https://hermes.phinergy.biz/api"

class Economics:
    
    def __init__(self, session):
        self.session = session
        self.url = f'{base_url}/economics'
        self.economics = None
        
    def get_economics(self, unit_name, startdate, stopdate):
        """
        Retrieves economics data for a specific unit within a given time range.
        Args:
            unit_name (str): The name of the unit for which economics data is to be retrieved.
            startdate (datetime): The start date for the data retrieval.
            stopdate (datetime): The stop date for the data retrieval.

        Returns:
            pd.DataFrame: The economics data in a pandas DataFrame format.
        """
        
        
        startdate = hutils.formatting_date(startdate)
        stopdate = hutils.formatting_date(stopdate)
                                           
        payload = {
            "from": startdate.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "to": stopdate.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "unit": unit_name
        }
        
        response = self.session.request('get', self.url, params=payload)
        
        hutils.check_status(response)
        
        json_response = response.json()
        data = json_response['data'] 
        self.economics = pd.DataFrame(data)                            
        return self.economics
        

        
